package util;

public class BinarySearch {
	
	public boolean binarySearch(int[]data,int size,int key) {
		
         int low = 0;
         int high = size - 1;
          
         while(high >= low) {
             int middle = (low + high) / 2;
             if(data[middle] == key) {
                 return true;
             }
             if(data[middle] < key) {
                 low = middle + 1;
             }
             if(data[middle] > key) {
                 high = middle - 1;
             }

         }
        return false;
   }
}
