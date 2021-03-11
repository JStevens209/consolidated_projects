package ArrayQueue;
/**
 *
 * @author joshua
 */
public class Exceptions {
	
	public static class InvalidDataException extends Exception {
		public InvalidDataException( String e ) {
			super(e);
		}
	};
	
	public static class QueueEmptyException extends Exception {
		public QueueEmptyException( String e ) {
			super(e);
		}
	}
}
