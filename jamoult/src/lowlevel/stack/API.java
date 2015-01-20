package lowlevel.stack;

import java.util.function.Consumer;

import model.reconfunits.DSUThread;

public class API {
	/* Suspend the given thread */
	public static void suspendThread(DSUThread thread) {
		thread.suspend();
	}
	
	/* Resume the given thread */
	public static void resumeThread(DSUThread thread) {
		thread.resume();
	}
	
	/* Changes the "main" function of the given thread */
	public static void switchMain(DSUThread thread,Consumer<Object[]> func, Object[] args) {
	    thread.setMain(() -> func.accept(args));
	}
	
	/* Reboots the given thread */
	public static void resetThread(DSUThread thread) {
		thread.reset();
	}
}
