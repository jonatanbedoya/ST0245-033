/**
 * Programa que muestra la manera en la que se utilizan
 * permutaciones en la vida diaria.
 * @author Jonatan and Andrés
 */
import java.util.*;
class taller3{
  public static void main(String[] args) {
    try (Scanner e = new Scanner(System.in)) {
		System.out.print("Ingrese por favor el número de fichas en el juego: ");
		int f = e.nextInt();
		String a1 = "T1";
		String b1 = "T2";
		String c1 = "T3";
		TowerHanoi(f,a1,b1,c1);
    	/**System.out.print("Ingrese una cadena de texto, por favor: ");
    	String cadena = e.nextLine();
    	perm(cadena,"");*/
	  }
  }
  /** Programa que muestra la manera de mover una ficha
	 * en el juego de Torres de Hanoi con tres torres y n fichas.
	 * @author Jonatan and Andrés
   */
	public static void TowerHanoi(int n, String a, String b,String c) {
		if(n<=0) {
			System.out.println("Sin movimientos");
		}else if(n==1) {
			System.out.println("Por favor mover: "+a+" a posición: "+c);
		}else {
			TowerHanoi(n-1,a,c,b);
			System.out.println("Por favor mover: "+a+" a posición: "+c);
			TowerHanoi(n-1,b,a,c);
			}
	}
	/**
	 public static void perm(String s, String str) {
		 int cont = 0;
			int n = s.length();
			if (n<=0) {
			    System.out.println(s);
			}else {
			    for (int i = 0; i<n; i++) {
			    	for(int j=0;j<n;j++) {
			    		str = s.charAt(j)+str; 
			    		if(str.charAt(j)==str.charAt(i)) {
			    			cont++;
			    			}
			    		}
			    	}
			    }
			}*/
}
