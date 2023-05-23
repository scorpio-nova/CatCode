import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.BinaryExpr;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.util.ArrayList;

public class ModifyCondition extends VoidVisitorAdapter<Object> {
    private final Common mCommon;
    private File mJavaFile = null;
    private String mSavePath = "";
    private final ArrayList<Node> mOperatorNodes = new ArrayList<>();

    ModifyCondition() {
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
        locateOperators(com);
        mCommon.applyToPlace(this, mSavePath, com, mJavaFile, mOperatorNodes);
        super.visit(com, obj);
    }

    private void locateOperators(CompilationUnit com) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node instanceof BinaryExpr && isAugmentationApplicable(((BinaryExpr) node).getOperator())) {
                    mOperatorNodes.add(node);
                }
            }
        }.visitPreOrder(com);
        //System.out.println("OperatorNodes : " + mOperatorNodes.size());
    }

    public CompilationUnit applyTransformation(CompilationUnit com, Node opNode) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node.equals(opNode)) {
                    BinaryExpr replNode = (BinaryExpr) opNode.clone();
                    switch (((BinaryExpr) node).getOperator()) {
                        case LESS:
                            replNode.setOperator(BinaryExpr.Operator.LESS_EQUALS);
                            break;
                        case LESS_EQUALS:
                            replNode.setOperator(BinaryExpr.Operator.LESS);
                            break;
                        case GREATER:
                            replNode.setOperator(BinaryExpr.Operator.GREATER_EQUALS);
                            break;
                        case GREATER_EQUALS:
                            replNode.setOperator(BinaryExpr.Operator.GREATER);
                            break;
                        case EQUALS:
                            replNode.setOperator(BinaryExpr.Operator.NOT_EQUALS);
                        case NOT_EQUALS:
                            replNode.setOperator(BinaryExpr.Operator.EQUALS);
                        case OR:
                            replNode.setOperator(BinaryExpr.Operator.AND);
                        case AND:
                            replNode.setOperator(BinaryExpr.Operator.OR);
                        case PLUS:
                            replNode.setOperator(BinaryExpr.Operator.MINUS);
                        case MULTIPLY:
                            replNode.setOperator(BinaryExpr.Operator.DIVIDE);
                            break;
                    }
                    node.replace(replNode);
                }
            }
        }.visitPreOrder(com);
        return com;
    }

    private boolean isAugmentationApplicable(BinaryExpr.Operator op) {
        switch (op) {
            case LESS:
            case LESS_EQUALS:
            case GREATER:
            case GREATER_EQUALS:
            case EQUALS:
            case NOT_EQUALS:
            case OR:
            case AND:
            case PLUS:
            case MULTIPLY:
                return true;
        }
        return false;
    }

}
