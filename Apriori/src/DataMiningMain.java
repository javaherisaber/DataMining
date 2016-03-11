import java.io.InputStreamReader;
import java.util.ArrayList;

import database.AprioriDataset;
import frequentPattern.Apriori;
import frequentPattern.FrequentItemSet;

public class DataMiningMain {
	public static void main(String[] args) {
		
		System.out.println("**************************************************");
		System.out.println("*************** Mahdi Javaheri Saber *************");
		System.out.println("********* Apriori Algorithm demonstration ********");
		System.out.println("**************************************************");
		System.out.print("\n");
		System.out.println("*************** Input Database *******************");
		System.out.print("Items symbolTable = {");
		for (int i = 0; i < AprioriDataset.ITEMS.length; i++) {
			System.out.print("I"+AprioriDataset.ITEMS[i]);
			if(i != AprioriDataset.ITEMS.length-1)
				System.out.print(",");
		}
		System.out.print("}\n\n");
		System.out.println("TransactionID      ItemSet");
		System.out.println("--------------------------");
		for (int i = 0; i < AprioriDataset.TRANSACTIONS.length; i++) {
			System.out.print("     T" + i + "            ");
			for (int j = 0; j < AprioriDataset.TRANSACTIONS[i].length; j++) {
				System.out.print("I"+AprioriDataset.TRANSACTIONS[i][j]);
				if(j != AprioriDataset.TRANSACTIONS[i].length-1)
					System.out.print(",");
			}
			System.out.println();
		}
		System.out.println("**************************************************");
		System.out.println();
		System.out.println("*********** Frequent ItemSet Table ***************");
		
		Apriori apriori = new Apriori();
		ArrayList<ArrayList<FrequentItemSet>> frequentItemSets = apriori.aprioriAlgorithm(AprioriDataset.ITEMS, AprioriDataset.TRANSACTIONS, 2);
		int indexTopLevel = 0;
		for (ArrayList<FrequentItemSet> arrayList : frequentItemSets) {
			System.out.print("LargeSet No " + indexTopLevel + " = {");
			int indexSecondLevel = 0;
			for (FrequentItemSet frequentItemSet : arrayList) {
				System.out.print("{");
				for (int i = 0; i < frequentItemSet.itemSet.length; i++) {
					System.out.print("I"+frequentItemSet.itemSet[i]);
				}
				System.out.print("}=>cnt:" + frequentItemSet.count);
				if(indexSecondLevel != (arrayList.size() - 1))
					System.out.print(",");
				indexSecondLevel++;
			}
			System.out.println("}");
			indexTopLevel++;
		}
		InputStreamReader isr = new InputStreamReader(System.in);
	}
}
