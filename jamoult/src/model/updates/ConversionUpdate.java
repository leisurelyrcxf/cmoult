package model.updates;

import static lowlevel.data_update.API.updateToClass;
import model.ReconfUnit;
import model.Update;
import model.UpdateFunction;

public abstract class ConversionUpdate<T1 extends ReconfUnit, T2 extends ReconfUnit> extends Update {
	protected Class<T1> cls;
	protected Class<T2> new_cls;
	protected UpdateFunction transformer;

	public ConversionUpdate(String name,Class<T1> cls, Class<T2> new_cls,UpdateFunction transformer) {
		super(name);
		this.cls = cls;
		this.new_cls = new_cls;
		this.transformer = transformer;
	}
	
	protected UpdateFunction getTransformer() {
		return (obj) -> updateToClass(obj, this.new_cls, this.transformer);
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
	public boolean over() {
		return true;
	}
}