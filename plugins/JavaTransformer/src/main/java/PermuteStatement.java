import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.stmt.EmptyStmt;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class PermuteStatement extends VoidVisitorAdapter<Object> {
    private final Common mCommon;
    private File mJavaFile = null;
    private String mSavePath = "";
    private ArrayList<ArrayList<Node>> mBasicBlockNodes = new ArrayList<>();
    private final ArrayList<Node> mDummyNodes = new ArrayList<>();

    PermuteStatement() {
        //System.out.println("\n[ PermuteStatement ]\n");
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
        mBasicBlockNodes = locateBasicBlockStatements(com);
        mDummyNodes.add(new EmptyStmt());
        mCommon.applyToPlace(this, mSavePath, com, mJavaFile, mDummyNodes);
        super.visit(com, obj);
    }

    private ArrayList<ArrayList<Node>> locateBasicBlockStatements(CompilationUnit com) {
        ArrayList<Node> innerStatementNodes = new ArrayList<>();
        ArrayList<ArrayList<Node>> basicBlockNodes = new ArrayList<>();
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node instanceof Statement) {
                    if (node instanceof ExpressionStmt
                            && node.findAll(MethodCallExpr.class).size() == 0
                            && !mCommon.isNotPermeableStatement(node)) {
                        innerStatementNodes.add(node);
                    } else {
                        if (innerStatementNodes.size() > 1) {
                            basicBlockNodes.add(new ArrayList<>(innerStatementNodes));
                        }
                        innerStatementNodes.clear();
                    }
                }
            }
        }.visitBreadthFirst(com);
        return basicBlockNodes;
    }

    public CompilationUnit applyTransformation(CompilationUnit com) {
        int cnt = 0;
        for (int k = 0; k < mBasicBlockNodes.size(); k++) {
            ArrayList<Node> basicBlockNodes = mBasicBlockNodes.get(k);
            for (int i = 0; i < basicBlockNodes.size(); i++) {
                for (int j = i + 1; j < basicBlockNodes.size(); j++) {
                    Statement stmt_i = (Statement) basicBlockNodes.get(i);
                    Statement stmt_j = (Statement) basicBlockNodes.get(j);
                    if (stmt_i.getParentNode().equals(stmt_j.getParentNode())) {
                        List<SimpleName> iIdentifiers = stmt_i.findAll(SimpleName.class);
                        List<SimpleName> jIdentifiers = stmt_j.findAll(SimpleName.class);
                        List<SimpleName> ijIdentifiers = iIdentifiers.stream()
                                .filter(jIdentifiers::contains).collect(Collectors.toList());
                        if (ijIdentifiers.size() == 0) { //dependency check between i & j statement
                            List<SimpleName> bIdentifiers = new ArrayList<>();
                            for (int b = i + 1; b < j; b++) {
                                Statement stmt_b = (Statement) basicBlockNodes.get(b);
                                bIdentifiers.addAll(stmt_b.findAll(SimpleName.class));
                            }
                            List<SimpleName> ibIdentifiers = iIdentifiers.stream()
                                    .filter(bIdentifiers::contains).collect(Collectors.toList());
                            if (ibIdentifiers.size() == 0) { //dependency check among i & internal statements
                                List<SimpleName> jbIdentifiers = jIdentifiers.stream()
                                        .filter(bIdentifiers::contains).collect(Collectors.toList());
                                if (jbIdentifiers.size() == 0) { //dependency check among j & internal statements
                                    swapStatementNodes(com, k, i, j, ++cnt);
                                }
                            }
                        }
                    }
                }
            }
        }
        return null;
    }

    private void swapStatementNodes(CompilationUnit com, int k, int i, int j, int cnt) {
        CompilationUnit newCom = com.clone();
        ArrayList<ArrayList<Node>> statementNodes = locateBasicBlockStatements(newCom);
        Statement stmt_i = (Statement) statementNodes.get(k).get(i);
        Statement stmt_j = (Statement) statementNodes.get(k).get(j);
        stmt_i.replace(stmt_j.clone());
        stmt_j.replace(stmt_i.clone());
        mCommon.saveTransformation(mSavePath, newCom, mJavaFile, String.valueOf(cnt));
    }

}
