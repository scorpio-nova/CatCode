package Utils;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.nodeTypes.NodeWithSimpleName;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;

public class VariableNameExtractor {

    public static void main(String[] args) {
        String filePath = "/Users/serena/Desktop/THU/01-博一上/AI-Code/java-example/RawCode";
        JSONArray arr = new JSONArray();
        for (int i = 0; i < 164; i++) {
            String fileName = "solution-" + i + ".java";
            System.out.println("filename:"+fileName);
            JSONObject obj = extractMethods(filePath, fileName);
            arr.put(obj);
        }


    }
    public static JSONObject extractMethods(String filePath, String fileName) {
        try {
            File sourceFile = new File(filePath + "/" + fileName);
            String sourceCode = IOUtils.toString(new FileReader(sourceFile));

            JSONArray methodArray = extractVariables(sourceFile);
            JSONObject result = new JSONObject();
            result.put("source_file", sourceFile);
            result.put("source_code", sourceCode);
            result.put("methods", methodArray);
            writeToJSONFile(result, filePath, fileName);
            return result;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void extractVariables(String javaCode) {
        try {
            CompilationUnit compilationUnit = new JavaParser().parse(new StringReader(javaCode)).getResult().get();
            new VariableVisitor().visit(compilationUnit, null);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static JSONArray extractVariables(File inputFile) {
        try {
            CompilationUnit compilationUnit = new JavaParser().parse(inputFile).getResult().get();
            JSONArray methodArray = new JSONArray();
            new VariableVisitor().visit(compilationUnit, methodArray);
            return methodArray;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    private static class VariableVisitor extends VoidVisitorAdapter<JSONArray> {
        @Override
        public void visit(MethodDeclaration methodDeclaration, JSONArray methodArray) {
            super.visit(methodDeclaration, methodArray);
            JSONObject method = new JSONObject();
            System.out.println("Method name: " + methodDeclaration.getName());
            method.put("method_name", methodDeclaration.getName().asString());
            System.out.println("Method parameters: " + methodDeclaration.getParameters());
            method.put("method_parameters", methodDeclaration.getParameters().stream().map(NodeWithSimpleName::getNameAsString).toArray());
            JSONArray variableArray = new JSONArray();
            new VariableDeclaratorVisitor().visit(methodDeclaration, variableArray);
            method.put("variables", variableArray);
            methodArray.put(method);

        }
    }

    private static class VariableDeclaratorVisitor extends VoidVisitorAdapter<JSONArray> {
        @Override
        public void visit(VariableDeclarator variableDeclarator, JSONArray variableArray) {
            variableArray.put(variableDeclarator.getName());
        }
    }

    private static void writeToJSONFile(JSONObject json, String filePath, String fileName) throws IOException {
        FileWriter file = new FileWriter(filePath + "/" + fileName.replace(".java", ".json"));
        file.write(json.toString());
        file.flush();
        file.close();
    }
}
