package model.managers;

import java.util.List;

import model.Application;
import model.Manager;
import model.Update;
import model.basics.Event;
import model.reconfunits.DSUThread;

/**
 * Manager using its owwn thread to monitor alterabilty and apply the update. No
 * to be used! For inheritance only! 
 */
public abstract class ThreadedManager extends Manager {

	private Thread thread;
	private boolean stopped = false;
	private int sleepTime = 2;
	private final Event invoked = new Event();
	private final Event over  = new Event();
	private Update currentUpdate; 

	public ThreadedManager(String name, Application appli, List<DSUThread> threads) {
		super(name, appli, threads);
		this.thread = new Thread(() -> this.thread_main());
	}

	public void setSleepTime(int sleepTime) {
	    this.sleepTime = sleepTime;
	}
	    
	public void addUpdate(Update update) {
	    super.addUpdate(update);
	    this.invoked.set();
	}

	public void start() {
		this.thread.start();
	}
	
	/** Indicates that the update is complete */
	public void finish() {
	    this.over.set();
	    if (this.pendingUpdates.isEmpty()) 
	        this.invoked.clear();
	}

	/** Waits for the update to be complete 
	 * @throws InterruptedException */
	public void waitForUpdate() throws InterruptedException {
	    this.over.doWait();
	}

	protected void thread_main() {
		while (!this.stopped) {
			try {
				this.invoked.doWait();
				// there is some pending updates
				Thread.sleep(this.sleepTime);
				if (this.currentUpdate == null)
					this.currentUpdate = this.pendingUpdates.poll();
				this.over.clear();
				if (!this.currentUpdate.isApplied()) {
					if (this.currentUpdate.requirements() && this.currentUpdate.alterability()) {
		                this.pauseActiveUnits();
		                this.currentUpdate.apply();
		                this.resumeActiveUnits();
		                this.currentUpdate.setApplied();
					}
				};
		        if (this.currentUpdate.isApplied()) {
		            if (this.currentUpdate.over()) {
		            	this.appli.addCompletedUpdate(this.currentUpdate.getName());
		                this.currentUpdate = null;
		                this.finish();
		            }
		        }
			} catch (InterruptedException e) {
				this.stopped = true;
			}
		}
	}
}