package model.updates;

import model.Update;
import model.basics.Function;
import model.basics.Module;
import static lowlevel.alterability.API.isFunctionInAnyStack;
import static lowlevel.relinking.API.redefineFunction;

public class SafeRedefineUpdate extends Update {

	private Module module;
	private Function function;
	private Function new_function;

	public SafeRedefineUpdate(Module module,Function function, Function new_function) {
		super("SafeRedefineUpdate");
		this.module = module;
		this.function = function;
		this.new_function = new_function;
	}

	@Override
	public boolean requirements() {
		return true;
	}

	@Override
	public boolean alterability() {
		return isFunctionInAnyStack(this.function, this.manager.getThreads());
	}

	@Override
	public void apply() {
		redefineFunction(this.module,this.function,this.new_function);
	}

	@Override
	public boolean over() {
		return true;
	}
}
