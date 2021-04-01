package project6;


public class ListBinaryTree implements BinaryTree {

	private STNode root;
	private int size;
	
    public void fillTree() {
		
        root = new STNode(0, null, null, null);
        STNode node1 = new STNode(1, root, null, null);
        STNode node2 = new STNode(2, root, null, null);
        root.setLeftChild(node1);
        node1.setSibling(node2);

        STNode node3 = new STNode(3, node1, null, null);
        STNode node4 = new STNode(4, node1, null, null);
        node1.setLeftChild(node3);
        node3.setSibling(node4);

        STNode node5 = new STNode(5, node2, null, null);
        STNode node6 = new STNode(6, node2, null, null);
        node2.setLeftChild(node5);
        node5.setSibling(node6);

        STNode node7 = new STNode(7, node3, null, null);
        STNode node8 = new STNode(8, node3, null, null);
        node3.setLeftChild(node7);
        node7.setSibling(node8);

        STNode node9 = new STNode(9, node4, null, null);
        STNode node10 = new STNode(10, node4, null, null);
        node4.setLeftChild(node9);
        node9.setSibling(node10);

        size = 11;
    }
    public static void main (String[] args) {
        ListBinaryTree myTree = new ListBinaryTree();
        myTree.fillTree();
						
		PreorderWalk preorder = new PreorderWalk( myTree );
		InorderWalk inorder = new InorderWalk( myTree );
		PostorderWalk postorder = new PostorderWalk( myTree );
		
		System.out.println( "Preorder: " );
		preorder.execute( myTree.root() );
		
		System.out.println( "Inorder: " );
		inorder.execute( myTree.root() );
		
		System.out.println( "Postorder: ");
		postorder.execute( myTree.root() );
		
		/**
		 * Print Readout:
		    Preorder: 
			0
			1
			3
			4
			2
			Inorder: 
			3
			1
			4
			0
			2
			Postorder: 
			3
			4
			1
			2
			0
		 */
    }
	
	@Override
	public Position root() throws EmptyTreeException {
		if( size == 0 ) {
			throw new EmptyTreeException( "ERROR: Tree is empty, no root." );
		}
		return root;
	}
	
	@Override
	public Position leftChild ( Position pos ) throws InvalidPositionException {
		isValidPos( pos );
		
		return ((STNode) pos).getLeftChild();
	}
	
	@Override
	public Position rightChild (Position pos) throws InvalidPositionException {
		isValidPos( pos );
		
		if( ((STNode) pos).getLeftChild() != null ) {
			return ((STNode) pos).getLeftChild().getSibling();
		}
		
		return null;
	}
	
	@Override
	public Position sibling (Position pos) throws InvalidPositionException {
		isValidPos( pos );
	
		if( ((STNode) pos).getSibling() != null ) {
			return ((STNode) pos).getSibling();
		}
		else if( ((STNode) pos).getParent() != null ) {
			return ((STNode) pos).getParent().getLeftChild();
		}

		return null;
	}
	
	@Override
	public Position parent(Position pos) throws InvalidPositionException {
		isValidPos( pos );
		
		return ((STNode) pos).getParent();
	}
	
	@Override
	public boolean isInternal (Position pos) throws InvalidPositionException {
		isValidPos( pos );
		
		return ((STNode) pos).getLeftChild() != null;
	}
	
	@Override
	public boolean isExternal (Position pos) throws InvalidPositionException {
		isValidPos( pos );
		
		return ((STNode) pos).getLeftChild() == null;
	}
	
	@Override
	public boolean isRoot (Position pos) throws InvalidPositionException {
		isValidPos( pos );
		
		return ((STNode) pos).getParent() == null;
	}
	
	@Override
	public int size() {
		return size;
	}
	
	@Override
	public boolean isEmpty() {
		return size == 0;
	}
	
	private void isValidPos( Position pos ) throws InvalidPositionException {
		if( !(pos instanceof STNode) ) {
			throw new InvalidPositionException( "ERROR: Given position, not instance of STNode" );
		}
	}
}