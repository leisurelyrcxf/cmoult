package lowlevel.relinking;

import model.basics.Function;
import model.basics.Module;

public class API {
	public static void redefineFunction(Module module, Function function, Function new_function) {
		module.redefineFunction(function, new_function);
	}
}
