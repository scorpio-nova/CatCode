package Utils;

import com.github.javaparser.JavaParser;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

public class VariableComparer {
    public static CompilationUnit getParseUnit(File javaFile) {
        CompilationUnit root = null;
        try {
            StaticJavaParser.getConfiguration().setAttributeComments(false);
            String txtCode = new String(Files.readAllBytes(javaFile.toPath()));
            if (!txtCode.startsWith("class")) txtCode = "class T { \n" + txtCode + "\n}";
            root = StaticJavaParser.parse(txtCode);
        } catch (Exception ignore) {}
        return root;
    }

    public static void main(String[] args) throws Exception {
        // Set the path
        String baseFilePath = "/Users/serena/Desktop/THU/01-博一上/AI-Code/java-example/RawCode/";
        String modifiedFilePath = "/Users/serena/Desktop/THU/01-博一上/AI-Code/java-example/VariableRandomRenaming/";

        // Set the range of n
        int nMin = 0;
        int nMax = 163;
        int kMax = 3;

        JSONObject fileInfos = new JSONObject();

        // Iterate over the range of n
        for (int n = nMin; n <= nMax; n++) {

            // Set the base file name
            String baseFileName = "solution-" + n + ".java";

            // Parse the base file
            File baseFile = new File(baseFilePath+baseFileName);
            if (!baseFile.exists()) {
                System.out.println("File not found: " + baseFile);
                continue;
            }
            CompilationUnit baseCu = getParseUnit(baseFile);

            // Extract the variable names from the base file
            List<String> baseVariableNames = new ArrayList<>();
            baseCu.findAll(MethodDeclaration.class).forEach(vd -> baseVariableNames.add(vd.getNameAsString()));
            baseCu.findAll(Parameter.class).forEach(vd -> baseVariableNames.add(vd.getNameAsString()));
            baseCu.findAll(VariableDeclarator.class).forEach(vd -> baseVariableNames.add(vd.getNameAsString()));

            StringBuilder underlineFileName = new StringBuilder();
            // Iterate over the range of k

            JSONObject fileVariables = new JSONObject();
            for (int k = 1; k <= kMax; k++) {
                underlineFileName.append("_").append(k);
                String modifiedFileName = baseFileName.substring(0, baseFileName.lastIndexOf(".")) + underlineFileName + ".java";

                // Parse the modified file
                File modifiedFile = new File(modifiedFilePath+k+"-transform/"+modifiedFileName);
                if (!modifiedFile.exists()) {
                    System.out.println("File not found: " + modifiedFile);
                    break;
                }
                CompilationUnit modifiedCu = getParseUnit(modifiedFile);
                // Extract the variable names from the modified file
                List<String> modifiedVariableNames = new ArrayList<>();
                // add method parameters and variable names
                modifiedCu.findAll(MethodDeclaration.class).forEach(vd -> modifiedVariableNames.add(vd.getNameAsString()));
                modifiedCu.findAll(Parameter.class).forEach(vd -> modifiedVariableNames.add(vd.getNameAsString()));
                modifiedCu.findAll(VariableDeclarator.class).forEach(vd -> modifiedVariableNames.add(vd.getNameAsString()));
                System.out.println("Base file: " + baseFileName);
                System.out.println("Modified file: " + modifiedFileName);
                System.out.println("baseVariableNames: " + baseVariableNames);
                System.out.println("modifiedVariableNames: " + modifiedVariableNames);

                // Compare the extracted variable names and store the new and old variable names
                JSONArray variablePairs = new JSONArray();
                int len = Math.min(baseVariableNames.size(), modifiedVariableNames.size());
                for (int i = 0; i < len; i++) {
                    String baseVariableName = baseVariableNames.get(i);
                    String modifiedVariableName = modifiedVariableNames.get(i);
                    if (!baseVariableName.equals(modifiedVariableName)) {
                        JSONObject variablePair = new JSONObject();
                        variablePair.put("old", baseVariableName);
                        variablePair.put("new", modifiedVariableName);
                        variablePairs.put(variablePair);
                    }
                }
                fileVariables.put(k+"-transform", variablePairs);
            }
            fileInfos.put(baseFileName,fileVariables);
        }

        // Write the extracted variables to a JSON file
        FileWriter fileWriter = new FileWriter(modifiedFilePath+"variables.json");
        fileWriter.write(fileInfos.toString(4));
        fileWriter.flush();
        fileWriter.close();
    }
}

