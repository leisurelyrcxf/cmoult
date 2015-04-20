package lowlevel.alterability;

import java.util.List;

import model.basics.Function;
import model.reconfunits.DSUThread;

public class API {
	/** Takes a function and a thread object as arguments. Returns true if
	 * the function is in the stack of the given thread, false either. */
	public static boolean isFunctionInStack(Function func, DSUThread thread) {
	    return thread.isActiveFunction(func);
	}
	/** Takes a function as argument and a list of threads. Returns true if
	 *  the function is in the stack of any of the given threads, false either. */
	public static boolean isFunctionInAnyStack(Function func, List<DSUThread> threads) {
		for (DSUThread t : threads)
			if (t.isActiveFunction(func))
				return true;
	    return false;
	}
}
