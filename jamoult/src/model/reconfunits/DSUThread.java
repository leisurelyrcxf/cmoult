package model.reconfunits;

import model.ActiveReconfUnit;
import model.basics.Function;

public class DSUThread extends ActiveReconfUnit {
	private Thread thread;

	public DSUThread(Runnable main) {
		super(main);
	}

	@Override
	public void suspend() {
		this.thread.suspend();
	}

	@Override
	public void resume() {
		this.thread.resume();
	}

	@Override
	public void reset() {
		this.thread.stop();
		thread = new Thread(this.main);
		thread.start();
	}

	@Override
	public boolean isActiveFunction(Function func) {
		// TODO Auto-generated method stub
		return false;
	}
	
	

}
