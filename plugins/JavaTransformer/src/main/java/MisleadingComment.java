import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.stmt.EmptyStmt;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.ast.comments.JavadocComment;
import org.json.JSONArray;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Random;

public class MisleadingComment extends VoidVisitorAdapter<Object> {
    private final Common mCommon;
    private File mJavaFile = null;
    private String mSavePath = "";
    private final ArrayList<Node> mDummyNodes = new ArrayList<>();

    MisleadingComment() {
        //System.out.println("\n[ MisleadingComment ]\n");
        mCommon = new Common();
    }

    public void inspectSourceCode(File javaFile) {
        this.mJavaFile = javaFile;
        mSavePath = Common.mRootOutputPath + this.getClass().getSimpleName() + "/";
        CompilationUnit root = mCommon.getParseUnit(mJavaFile);
        if (root != null) {
            this.visit(root.clone(), null);
        }
    }

    @Override
    public void visit(CompilationUnit com, Object obj) {
        mDummyNodes.add(new EmptyStmt());
        mCommon.applyToPlace(this, mSavePath, com, mJavaFile, mDummyNodes);
        super.visit(com, obj);
    }

    public CompilationUnit applyTransformation(CompilationUnit com) {
//        if (com.findFirst(MethodDeclaration.class).isPresent() &&
//                com.findFirst(MethodDeclaration.class).flatMap(MethodDeclaration::getBody).isPresent()) {
//            BlockStmt blockStmt = new BlockStmt();
//            for (Statement statement : com.findFirst(MethodDeclaration.class)
//                    .flatMap(MethodDeclaration::getBody).get().getStatements()) {
//                blockStmt.addStatement(statement);
//            }
//            blockStmt.addStatement(0, getMisleadingComment());
            MethodDeclaration md = com.getType(0).getMethods().get(0);
            md.setComment(getMisleadingComment());
//        }
        return com;
    }

    private JavadocComment getMisleadingComment() {
        try{
            String fileName = "/Users/serena/Desktop/THU/01-博一上/AI-Code/CodeGeeX-main/codegeex/benchmark/humaneval-x/java/data/humaneval_java.json";
            // use library org.json to read the json file and read the field "text" of each json object
            ObjectMapper mapper = new ObjectMapper();

            // read the JSON file
            File jsonFile = new File(fileName);
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode root = objectMapper.readTree(jsonFile);

            // select a random comment from the JSON file
            Random rand = new Random();
            int randomIndex = rand.nextInt(root.size());
            String commentStr = root.get(randomIndex).get("text").asText();
            return new JavadocComment(commentStr);
        } catch (Exception e) {
            e.printStackTrace();
        }
        String commentStr = "// This is a misleading comment.";
        return new JavadocComment(commentStr);
    }

}
