package model;


/** Base Update class */
public abstract class Update {
	protected Manager manager;
	private final String name;
	private boolean applied = false;

	public Update(String name) {
        this.name = name;
	}

    public abstract boolean requirements();
    public abstract boolean alterability();
    public abstract void apply();
    public abstract boolean over();
 
	public void setManager(Manager manager) {
		this.manager = manager;
	}

	public boolean isApplied() {
		return this.applied;
	}

	public void setApplied() {
		this.applied = true;
	}

	public String getName() {
		return this.name;
	}
}
