import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.*;
import java.util.*;

public class VariableRenaming extends VoidVisitorAdapter<Object> {
    private final Common mCommon;
    private File mJavaFile = null;
    private String mSavePath = "";
    private final ArrayList<Node> mVariableNodes = new ArrayList<>();
    private String mNewVariableName = "";
    private String mRandomVariablePath = null;
    static boolean cleanVariableChangeFile = true;


    VariableRenaming() {
        //System.out.println("\n[ VariableRenaming ]\n");
        mCommon = new Common();
    }

    public void inspectSourceCode(File javaFile, String randomVariablePath) {
        this.mJavaFile = javaFile;
        mSavePath = Common.mRootOutputPath + this.getClass().getSimpleName() + "/";
        CompilationUnit root = mCommon.getParseUnit(mJavaFile);
        mRandomVariablePath= randomVariablePath;
        if (root != null) {
            this.visit(root.clone(), null);
        }
    }

    @Override
    public void visit(CompilationUnit com, Object obj) {
        if (mRandomVariablePath!= null) {
            String newName = selectVariableNameFromFile();
            locateRandomVariableRenaming(com,newName);
        }
        else locateVariableRenaming(com);
        mCommon.applyToPlace(this, mSavePath, com, mJavaFile, mVariableNodes);
        String javaFileName = mJavaFile.getName();
        appendVariableChangeToFile(mVariableNodes,mNewVariableName,javaFileName,mSavePath);
        super.visit(com, null);
    }

    private void locateVariableRenaming(CompilationUnit com) {
        final int[] variableId = {0};
        mNewVariableName = "var";
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (isTargetVariable(node)) {
                    mVariableNodes.add(node);
                    if (node.toString().equals(mNewVariableName)) {
                        variableId[0]++;
                        mNewVariableName = "var" + variableId[0];
                    }
                }
            }
        }.visitPreOrder(com);
        //System.out.println("TargetVariable : " + mVariableList);
    }
    private void locateRandomVariableRenaming(CompilationUnit com,String newName) {
        final int[] variableId = {0};
        mNewVariableName = newName;
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (isTargetVariable(node)) {
                    mVariableNodes.add(node);
                    if (node.toString().equals(newName)) {
                        variableId[0]++;
                        System.out.println("11111111");
                        System.out.println(mNewVariableName);
                        mNewVariableName = newName + variableId[0];
                    }
                }
            }
        }.visitPreOrder(com);
    }

    private boolean isTargetVariable(Node node) {
        return (node instanceof SimpleName &&
                (node.getParentNode().orElse(null) instanceof Parameter
                        || node.getParentNode().orElse(null) instanceof VariableDeclarator));
    }

    public CompilationUnit applyTransformation(CompilationUnit com, Node varNode) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                String oldName = varNode.toString();
                if (node.toString().equals(oldName)) {
                    if (node instanceof SimpleName
                            && !(node.getParentNode().orElse(null) instanceof MethodDeclaration)
                            && !(node.getParentNode().orElse(null) instanceof ClassOrInterfaceDeclaration)) {
                        System.out.println("2222222");
                        System.out.println("oldName : " + oldName);
                        System.out.println("newName : " + mNewVariableName);
                        System.out.println("node : " + node);
                        ((SimpleName) node).setIdentifier(mNewVariableName);
                    }
                }
            }
        }.visitPreOrder(com);
        return com;
    }
    public String selectVariableNameFromFile() {
        List<String> variableList = new ArrayList<>();
        try {
            File variableSetFile = new File(mRandomVariablePath);
            System.out.println("Variable set file: " + variableSetFile.getName());
            Scanner scanner = new Scanner(variableSetFile);
            while (scanner.hasNextLine()) {
                variableList.add(scanner.nextLine());
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        Random random = new Random();
        int randomIndex = random.nextInt(variableList.size());
        System.out.println("randomIndex:"+randomIndex);
        String newVariableName = variableList.get(randomIndex);
        return newVariableName;
    }

    /**
     * Write the variable change to a JSON file to outputPath folder, each line is a JSON object with the following format:
     * {
     * "javaFileName": "xxx.java",
     * "oldVariableName": "xxx",
     * "newVariableName": "xxx"
     * }
     * @param sourceNodes the list of source nodes, each node is a variable, node.toString() is the variable name
     * @param targetName the new variable name
     * @param javaFileName the java file name
     * @param outputPath the output path
     */
    public void appendVariableChangeToFile(ArrayList<Node> sourceNodes,String targetName,String javaFileName, String outputPath){
        String outputFileName = outputPath + "variableChange.txt";
        if (cleanVariableChangeFile){
            File file = new File(outputFileName);
            if (file.exists()){
                file.delete();
            }
            cleanVariableChangeFile = false;
        }
        try {
            FileWriter fw = new FileWriter(outputFileName,true);
            int i = 0;
            for (Node node : sourceNodes) {
                i++;
                String sourceName = node.toString();
                fw.write("{\"javaFileName\": \"" + javaFileName.substring(0,javaFileName.lastIndexOf("."))+"_"+i+".java" + "\", \"oldVariableName\": \"" + sourceName + "\", \"newVariableName\": \"" + targetName + "\"}\n");
            }
            fw.flush();
            fw.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
