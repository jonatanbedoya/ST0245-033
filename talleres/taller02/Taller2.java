
public class Taller2 {

    /**
     * @param p entrada 1 entero positivo, mayor que q
     * @param q entrada 2 entero positivo, menor que p
     *
     * El método gcd tiene como objetivo ecnontrar el
     * máximo común divisor de dos números, por medio del
     * algoritmo de euclides
     * @see <a href="https://www.youtube.com/watch?v=Q9HjeFD62Uk"> Explicación </a>
     * @see <a href="https://visualgo.net/en/recursion"> Funcionamiento </a>
     *
     * @return el máximo común divisor
     */
    public static int gcd(int p,int q){
        if (q == 0){
            return p;
        }else{
            return gcd(q,p%q);
        }
    }

    /**
     * @param start entrada 1 entero positivo, determina un índice dentro del proceso
     * @param nums entrada 2 arreglo de enteros positivos, sobre el cual vamos a interar
     * @param target entrada 3 entero positivo, determina el valor de referencia
     * El método SumaGrupo tiene como objetivo darnos a conocer si hay
     * algun subconjunto el cual su suma = target.
     *
     *
     * @return verdadero si hay un subconjunto el cual su suma = target
     */
    public static boolean SumaGrupo(int start,int[]nums,int target){
        System.out.println(start + " "+ target);
        if (start >= nums.length) {
            if (target == 0)
                return true;
            else
                return false;
        }else{ // start < nums.length
            boolean universo1 = SumaGrupo(start + 1,nums,target - nums[start]);
            if (universo1)
                return true;
            else{
                boolean universo2 = SumaGrupo(start + 1,nums,target);
                if (universo2 == true)
                    return true;
                else
                    return false;
            }
        }
    }

    /**
     * @param s se trata de una cadena de caracteres sobre la cual hallaremos las posibles combinaciones.
     *
     * El método combinations se define para que solo se tenga que pasar el parametro s y no la cadena
     * vacía necesaria para el metodo reursivo combinationsAux. Este metodo no se modifica.
     *
     */
    public static void combinations(String s) {
        combinationsAux("", s);
    }

    /**
     * @param prefix, se utiliza como una variable auxiliar para guardar datos sobre el proceso.
     * @param s se trata de una cadena de caracteres sobre la cual hallaremos las posibles combinaciones.
     *
     *
     * El método combinationsAux se encarga de encontrar las posibles combinaciones en la cadena s
     * notese que el método es "private" de modo que solo se puede llamar desde el interior de la clase pues
     * el método que lo representa es combinations.
     * Para más detalles sobre modificadores de acceso:
     * @see <a href="http://ayudasprogramacionweb.blogspot.com/2013/02/modificadores-acceso-public-protected-private-java.html"> modificadores </a>
     *
     */

    private static void combinationsAux(String prefix, String s) {
        if(s.length() == 0) {
            System.out.println( ________ );
        }else{
            combinationsAux( _______ + s.charAt(0), s.substring(1));
            combinationsAux( prefix, s.substring( __ ));
        }
    }

}