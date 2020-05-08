package talleres;
import java.util.Arrays;

/**
 * La clase MiArrayList tiene la intención de representar un objeto que simule el comportamiento
 * de la clase ya implementada "ArrayList"
 * es claro que no se puede utilizar dicha estructura ya utilizada dentro de este ejercicio. 
 * Para más información de la clase ArrayList:
 * @see <a href="https://docs.oracle.com/javase/8/docs/api/java/util/ArrayList.html"> Ver documentacion ArrayList </a>
 * @author Mauricio Toro, Andres Paez
 * @version 1
 */
public class MiArrayList {
    private int size;
    private static final int DEFAULT_CAPACITY = 10;
    private int elements[];    
    /**
    * El metodo constructor se utiliza para incializar
    * variables a valores neutros como 0 o null.
    * El contructor no lleva parámetros en este caso.
    */
    public MiArrayList() {
        size = 0;
        elements = new int[DEFAULT_CAPACITY];
    } 
    /**
    * Tiene la intención de retornar la longitud del objeto
    * @return longitud del objeto
    * El size esta influenciado por las funciones add y del
    */
    public int size() {
        return size;
    }     
    private void agrandarlo(){
      int[] nuevo = int[elements.length*2];
      for (int i = 0; i < elements.length; i++)
        nuevo[i] = elements[i];
      elements = nuevo;
    }
    /** 
    * @param e el elemento a guardar
    * Agrega un elemento e a la última posición de la lista
    */
    public void add(int e) {
       if (size == elements.length)
           agrandarlo();  
       elements[size] = e;
    }
    /** 
    * @param i es un íncide donde se encuentra el elemento posicionado
    * Retorna el elemento que se encuentra en la posición i de la lista.
    */
    public int get(int i) throws Exception {
       if (i >= size || i < 0) // C1 es O(1)
         throw new Exception("Index out of bounds exception index = "+i); // C2 es O(1)
       else
        return elements[i]; // C3 es O(1)
       // T(n) = O(1) + O(1) = O(1)
    }
    /**
    * @param index es la posicion en la cual se va agregar el elemento
    * @param e el elemento a guardar
    * Agrega un elemento e en la posición index de la lista
    */
    public void add throw Exception(int index, int e) {
      if (index < 0)
         throw new Exception("Index out of bounds exception index = "+index);
      else
      elements[index] = e;
    } 

    /**
    * @param index es la posicion en la cual se va eliminar el elemento
    * ELimina el elemento  en la posición index de la lista
    */
    public void del throw Exception(int index){
      if (index < 0 || index==elements.length-1)
         throw new Exception("Index out of bounds exception index = "+index);
         else
         for(int i=index;i<elements.length;i++){
             elements[i] = elements[i+1];
           if(i==elements.length-1)
             elements[i] = null;
         }
    }
}
