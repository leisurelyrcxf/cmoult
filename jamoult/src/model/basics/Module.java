package model.basics;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class Module {

	public static Map<String,Module> modules = new HashMap<String, Module>();
	public static Module getModule(String name) {
		return modules.get(name);
	}

	private List<Attribute> attributes = new LinkedList<Attribute>();
	private List<Function> functions = new LinkedList<Function>();
	private String name;
	public Module(String name, List<Attribute> attributes, List<Function> functions) {
		this.name = name;
		this.attributes = attributes;
		this.functions = functions;
	}
	
	public List<Attribute> getAttrList() {
		return this.attributes;
	}

	public void redefineFunction(Function function, Function new_function) {
		for (Function f : this.functions)
			if (f.getName() == function.getName()) {
				functions.remove(function);
				functions.add(new_function);
			}
				
	}
}
