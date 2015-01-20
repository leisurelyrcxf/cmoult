package model.updates;

import lowlevel.data_access.Transformer;
import model.ReconfUnit;
import static lowlevel.data_access.API.startEagerUpdate;

/* Update to be used with the EagerConversionManager */
public class EagerConversionUpdate<T1 extends ReconfUnit,T2  extends ReconfUnit> extends ConversionUpdate<T1, T2> {
	/* Constructor. Takes the class of the objects to be updated, the new
    class to which they will be updated and a transformer function
    in its arguments */
	public EagerConversionUpdate(Class<T1> cls,Class<T2> new_cls,Transformer transformer) {
		super("EagerConversionUpdate",cls,new_cls,transformer);
	}

	@Override
	public void apply() {
		startEagerUpdate(this.cls, this.getTransformer());
	}
}
