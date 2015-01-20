package lowlevel.data_access;

import java.util.List;

import model.ReconfUnit;
import model.basics.Attribute;
import model.basics.Module;

public class API {
	/*
	 * Uses a data accessor to run an eager update. Takes the target class and
	 * the transformer function as argumments.
	 */
	public static <T extends ReconfUnit> void startEagerUpdate(Class<T> tclass,
			Transformer transformer) {
		Iterable<T> accessor = new DataAccessor<T>(tclass, Strategy.Immediate);
		for (T obj : accessor)
			transformer.transform(obj);
	}

	public static <T extends ReconfUnit> void setLazyUpdate(Class<T> tclass,
			Transformer transformer) {
		// TODO
	}
	
	/*
	 * Runs the given walker on the globals of the modules names in the
	 * module_names parameter. If this parameter is empty, it will default to
	 * the main module.
	 */
	public static void traverseHeap(HeapWalker walker, List<String> module_names) {
		List<String> ml = module_names;
		if (ml.isEmpty())
			ml.add("main");
		for (String name: ml) {
			Module m = Module.getModule(name);
			for (Attribute attr : m.getAttrList())
				walker.walk(attr.getValue());
		}
	}
}
