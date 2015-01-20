package model;

public class ReconfUnit {
	public void update(UpdateFunction f) {
		f.apply(this);
	}
}
