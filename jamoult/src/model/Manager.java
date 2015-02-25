package model;

import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import model.reconfunits.DSUThread;

/** An instance of a manager manages a set of reconfiguration units */
public abstract class Manager implements Runnable {
	/** The units managed by this manager */
	private List<? extends ReconfUnit> units;
	private String name;
	protected Queue<Update> pendingUpdates = new LinkedList<Update>();
	protected Application appli;
	
	public Manager(String name, Application appli, List<? extends ReconfUnit> units) {
		this.name = name;
        this.units = units;
        this.appli = appli;
        appli.register(this.name,this);
    }
	
	public void addUpdate(Update u) {
		this.pendingUpdates.add(u);
		u.setManager(this);
	}
	
	/* suspends all active units managed by the manager */
    public void pauseActiveUnits() {
    	for (ReconfUnit u : this.units)
    		if (u instanceof ActiveReconfUnit)
    			((ActiveReconfUnit) u).suspend();
    }

    /* resume the execution of all active units managed by the manager */
    public void resumeActiveUnits() {
    	for (ReconfUnit u : this.units)
    		if (u instanceof ActiveReconfUnit)
    			((ActiveReconfUnit) u).resume();
    }

	public void stop() { }

	public List<DSUThread> getThreads() {
		List<DSUThread> result = new LinkedList<DSUThread>();
		for (ReconfUnit u : this.units)
			if (u instanceof DSUThread)
				result.add((DSUThread) u);
		return result;
	}
}
