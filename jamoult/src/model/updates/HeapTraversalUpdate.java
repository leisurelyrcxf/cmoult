package model.updates;

import static lowlevel.data_access.API.traverseHeap;

import java.util.LinkedList;
import java.util.List;

import lowlevel.data_access.HeapWalker;
import model.Update;

/* Update to be used with HeapTraversalManager */
public class HeapTraversalUpdate extends Update {

	private HeapWalker walker;
	private List<String> modules = new LinkedList<String>();

	public HeapTraversalUpdate(HeapWalker walker, List<String> modules) {
		super("HeapTraversalUpdate");
		this.walker = walker;
		this.modules = modules;
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
		if (this.walker != null && !this.modules.isEmpty()) {
			traverseHeap(this.walker,this.modules);
		}
	}

	@Override
	public boolean over() {
		return true;
	}
}