package model.updates;

import java.util.function.Consumer;
import model.Update;
import model.reconfunits.DSUThread;
import static lowlevel.stack.API.switchMain;
import static lowlevel.stack.API.resumeThread;
import static lowlevel.stack.API.resetThread;


/* Update to be used with ThreadRebootManager */
public class ThreadRebootUpdate extends Update {

	private DSUThread thread;
	private Consumer<Object[]> new_main;
	private Object[] new_args;

	public ThreadRebootUpdate(DSUThread thread, Consumer<Object[]> new_main, Object[]new_args) {
		super("ThreadRebootUpdate");
	    this.thread = thread;
	    this.new_main = new_main;
	    this.new_args = new_args;
	}

	@Override
	public boolean requirements() {
		return true;
	}

	@Override
	public boolean alterability() {
		return true;
	}

	@Override
	public void apply() {
		resumeThread(this.thread);
		switchMain(this.thread,this.new_main,this.new_args);
	    resetThread(this.thread);
	}

	@Override
	public boolean over() {
		return true;
	}
	
}