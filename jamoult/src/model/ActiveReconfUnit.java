package model;

import model.basics.Function;

public abstract class ActiveReconfUnit extends ReconfUnit {
	
	public abstract void suspend();
	public abstract void resume();
	public abstract void reset();	
	protected Runnable main;
	
	public abstract boolean isActiveFunction(Function func);

	public void setMain(Runnable main) {
		this.main = main;
	}

	@Override
	public void update(UpdateFunction f) {
		this.suspend();
		f.apply(this);
		this.resume();
	}
	public ActiveReconfUnit(Runnable main) {
		this.main = main;
	}

}
