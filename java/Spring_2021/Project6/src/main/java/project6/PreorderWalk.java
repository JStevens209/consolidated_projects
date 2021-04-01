/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package project6;

/**
 *
 * @author joshua
 */
public class PreorderWalk extends EulerTour {
	
	PreorderWalk( BinaryTree tree ) {
		super(tree);
	}
	
	@Override
	protected void visitPreorder (Position pos, TraversalResult result) {
		System.out.println( pos.element() );
	}
	
	public void execute( Position startPos ) {
		this.performTour( startPos );
	}
}
