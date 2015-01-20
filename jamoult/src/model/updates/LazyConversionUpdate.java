package model.updates;

import model.ReconfUnit;
import model.UpdateFunction;
import static lowlevel.data_access.API.setLazyUpdate;


public class LazyConversionUpdate<T1 extends ReconfUnit,T2  extends ReconfUnit> extends ConversionUpdate<T1, T2> {
	public LazyConversionUpdate(Class<T1> cls,Class<T2> new_cls,UpdateFunction transformer) {
		super("LazyConversionUpdate",cls,new_cls,transformer);
	}

	@Override
	public void apply() {
		setLazyUpdate(this.cls,this.getTransformer());
	}

}