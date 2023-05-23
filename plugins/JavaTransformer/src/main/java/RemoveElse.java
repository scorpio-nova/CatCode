import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import java.io.File;
import java.util.ArrayList;

public class RemoveElse extends VoidVisitorAdapter<Object> {
    private final Common mCommon;
    private File mJavaFile = null;
    private String mSavePath = "";
    private final ArrayList<Node> mIfNodes = new ArrayList<>();

    RemoveElse() {
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
        locateConditionals(com);
        mCommon.applyToPlace(this, mSavePath, com, mJavaFile, mIfNodes);
        super.visit(com, obj);
    }

    private void locateConditionals(CompilationUnit com) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node instanceof IfStmt) {
                    IfStmt ifStmt = (IfStmt) node;
                    if (ifStmt.hasElseBranch()) {
                        mIfNodes.add(node);
                    }
                }
            }
        }.visitPreOrder(com);
    }

    public CompilationUnit applyTransformation(CompilationUnit com, Node ifNode) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node.equals(ifNode)) {
                    IfStmt ifStmt = (IfStmt) node;
                    ifStmt.getElseStmt().ifPresent(Node::remove);
                }
            }
        }.visitPreOrder(com);
        return com;
    }
}
