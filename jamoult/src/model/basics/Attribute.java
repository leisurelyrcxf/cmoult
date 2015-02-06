package model.basics;

public class Attribute {

	private String name;
	private Object value;
	public Attribute(String name, Object value) {
		this.name = name;
		this.value = value;
	}

	public Object getValue() {
		return this.value;
	}

}
