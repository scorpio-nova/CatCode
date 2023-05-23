import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class MethodRenaming extends VoidVisitorAdapter<Object> {
    private final Common mCommon;
    private File mJavaFile = null;
    private String mSavePath = "";
    private final ArrayList<Node> mMethodNodes = new ArrayList<>();
    private String mNewMethodName = "";
    private String mRandomMethodPath = null;

    MethodRenaming() {
        mCommon = new Common();
    }

    public void inspectSourceCode(File javaFile, String randomMethodPath) {
        this.mJavaFile = javaFile;
        mSavePath = Common.mRootOutputPath + this.getClass().getSimpleName() + "/";
        CompilationUnit root = mCommon.getParseUnit(mJavaFile);
        mRandomMethodPath = randomMethodPath;
        if (root != null) {
            this.visit(root.clone(), null);
        }
    }

    @Override
    public void visit(CompilationUnit com, Object obj) {
        locateMethodRenaming(com);
        mCommon.applyToPlace(this, mSavePath, com, mJavaFile, mMethodNodes);
        super.visit(com, obj);
    }

    private void locateMethodRenaming(CompilationUnit com) {
        final int[] methodId = {0};
        String newMethodName = "method";
        if (mRandomMethodPath != null) {
            List<String> methodList = new ArrayList<>();
            try {
                File methodSetFile = new File(mRandomMethodPath);
                System.out.println("Method set file: " + methodSetFile.getName());
                Scanner scanner = new Scanner(methodSetFile);
                while (scanner.hasNextLine()) {
                    methodList.add(scanner.nextLine());
                }
                scanner.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            Random random = new Random();
            int randomIndex = random.nextInt(methodList.size());
            newMethodName = methodList.get(randomIndex);
            System.out.println("New method name: " + newMethodName);
        }
        mNewMethodName = newMethodName;
        String finalNewMethodName = newMethodName;
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (isTargetMethod(node)) {
                    mMethodNodes.add(node);
                    if (node.toString().equals(mNewMethodName)) {
                        methodId[0]++;
                        mNewMethodName = finalNewMethodName + methodId[0];
                    }
                }
            }
        }.visitPreOrder(com);
    }

    private boolean isTargetMethod(Node node) {
        return (node instanceof MethodDeclaration);
    }

    public CompilationUnit applyTransformation(CompilationUnit com, Node methodNode) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node instanceof MethodDeclaration) {
                    System.out.println("Method name: " + ((MethodDeclaration) node).getName());
                    System.out.println("New method name: " + mNewMethodName);
                        ((MethodDeclaration) node).setName(mNewMethodName);
                    }
                }
            }.visitPreOrder(com);
        return com;
    }
}
