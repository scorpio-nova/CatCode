import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        /* arg[0]: root path for input folder, ie, ~/data/methods/
         * arg[1]: root path for output folder, ie, ~/data/transforms/
         *
         * extracted single method of project should be in 'methods' folder
         * separate folder for each refactoring will be created in 'transforms' folder
         */

        if (args.length == 2) {
            String inputPath = args[0];
            if (!inputPath.endsWith("/")) {
                inputPath += "/";
            }
            Common.mRootInputPath = inputPath;

            String outputPath = args[1];
            if (!outputPath.endsWith("/")) {
                outputPath += "/";
            }
            Common.mRootOutputPath = outputPath;

            inspectDataset();
        } else {
            String msg = "Error (args):" +
                    "\n\targ[0]: root path for input folder" +
                    "\n\targ[1]: root path for output folder";
            System.out.println(msg);
        }
    }

    private static void inspectDataset() {
        String input_dir = Common.mRootInputPath;
        ArrayList<File> javaFiles = new ArrayList<>(
                FileUtils.listFiles(
                        new File(input_dir),
                        new String[]{"java"},
                        true)
        );

        javaFiles.forEach((javaFile) -> {
            try {
                /** preprocess **/
                new ExtractMethod().inspectSourceCode(javaFile); // extract method names to a file


                /** equivalent */
                new NoTransform().inspectSourceCode(javaFile); // no transform
                /** token-level **/
                new VariableRenaming().inspectSourceCode(javaFile, null);
//                new MisleadingComment().inspectSourceCode(javaFile);
                /** control level **/
                new BooleanExchange().inspectSourceCode(javaFile);
                new LoopExchange().inspectSourceCode(javaFile);
                new UnusedStatement().inspectSourceCode(javaFile);
                new SwitchToIf().inspectSourceCode(javaFile);
                /** data level **/
                new ReorderCondition().inspectSourceCode(javaFile);
                new PermuteStatement().inspectSourceCode(javaFile);
                /** distinct */
                new RemoveElse().inspectSourceCode(javaFile);
                new ModifyCondition().inspectSourceCode(javaFile);
            } catch (Exception ex) {
                System.out.println("Exception: " + javaFile);
                ex.printStackTrace();
            }
        });
    }
}
