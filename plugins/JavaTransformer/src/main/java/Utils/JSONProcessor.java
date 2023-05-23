package Utils;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

public class JSONProcessor {
    public static void main(String[] args) throws IOException {
        String filePath = "/Users/serena/Desktop/THU/01-博一上/AI-Code/java-example/RawCode";
        combineJSONFiles(filePath);
        Set<String> variableSet = extractVariables(filePath);
        writeToFile(variableSet, filePath + "/variableSet.txt");
        Set<String> methodNameSet = extractMethodNames(filePath);
        writeToFile(methodNameSet, filePath + "/methodNameSet.txt");
        Set<String> methodParameterSet = extractMethodParameters(filePath);
        writeToFile(methodParameterSet, filePath + "/methodParameterSet.txt");
    }

    private static void combineJSONFiles(String filePath) throws IOException {
        JSONArray combinedArray = new JSONArray();
        for (int i = 0; i < 164; i++) {
            String fileName = "solution-" + i + ".json";
            JSONObject json = new JSONObject(new JSONTokener(new FileReader(filePath + "/" + fileName)));
            combinedArray.put(json);
        }
//        JSONObject combinedJson = new JSONObject();
//        combinedJson.put("solutions", combinedArray);
        FileWriter file = new FileWriter(filePath + "/combined.json");
        file.write(combinedArray.toString(4));
        file.flush();
        file.close();
    }

    private static Set<String> extractVariables(String filePath) throws IOException {
        JSONArray combinedJson = new JSONArray(new JSONTokener(new FileReader(filePath + "/combined.json")));
//        JSONArray solutions = combinedJson.getJSONArray("solutions");
        Set<String> variableSet = new HashSet<>();
        System.out.println("combinedJson.length(): "+combinedJson.length());
        for (int i = 0; i < combinedJson.length(); i++) {
            System.out.println("combinedJson.getJSONObject(i)"+combinedJson.getJSONObject(i));
            JSONArray methods = combinedJson.getJSONObject(i).getJSONArray("methods");
            for (int j = 0; j < methods.length(); j++) {
                JSONArray variables = methods.getJSONObject(j).getJSONArray("variables");
                for (int k = 0; k < variables.length(); k++) {
                    variableSet.add(variables.getString(k));
                }
            }
        }
        return variableSet;
    }
    private static Set<String> extractMethodNames(String filePath) throws IOException {
        JSONArray combinedJson = new JSONArray(new JSONTokener(new FileReader(filePath + "/combined.json")));
        Set<String> methodNameSet = new HashSet<>();
        for (int i = 0; i < combinedJson.length(); i++) {
            JSONArray methods = combinedJson.getJSONObject(i).getJSONArray("methods");
            for (int j = 0; j < methods.length(); j++) {
                methodNameSet.add(methods.getJSONObject(j).getString("method_name"));
            }
        }
        return methodNameSet;
    }

    private static Set<String> extractMethodParameters(String filePath) throws IOException {
        JSONArray combinedJson = new JSONArray(new JSONTokener(new FileReader(filePath + "/combined.json")));
        Set<String> methodParameterSet = new HashSet<>();
        for (int i = 0; i < combinedJson.length(); i++) {
            JSONArray methods = combinedJson.getJSONObject(i).getJSONArray("methods");
            for (int j = 0; j < methods.length(); j++) {
                JSONArray parameters = methods.getJSONObject(j).getJSONArray("method_parameters");
                for (int k = 0; k < parameters.length(); k++) {
                    methodParameterSet.add(parameters.getString(k));
                }
            }
        }
        return methodParameterSet;
    }

private static void writeToFile(Set<String> variableList, String fileName) throws IOException {
        FileWriter file = new FileWriter(fileName);
        for (String variable : variableList) {
            file.write(variable);
            file.write(System.lineSeparator());
        }
        file.flush();
        file.close();
    }
}
