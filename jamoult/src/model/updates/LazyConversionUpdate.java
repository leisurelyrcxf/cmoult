package model.updates;

import lowlevel.data_access.Transformer;
import model.ReconfUnit;
import static lowlevel.data_access.API.setLazyUpdate;


public class LazyConversionUpdate<T1 extends ReconfUnit,T2  extends ReconfUnit> extends ConversionUpdate<T1, T2> {
	public LazyConversionUpdate(Class<T1> cls,Class<T2> new_cls,Transformer transformer) {
		super("LazyConversionUpdate",cls,new_cls,transformer);
	}

	@Override
	public void apply() {
		setLazyUpdate(this.cls,this.getTransformer());
	}

}