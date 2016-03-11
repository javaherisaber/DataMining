package frequentPattern;

import java.util.ArrayList;

import util.BinarySearch;
import util.SortInteger;

public class Apriori {
	
	public ArrayList<ArrayList<FrequentItemSet>> aprioriAlgorithm(int[] items,int[][] dataSet,int minSupport){
		
		ArrayList<ArrayList<FrequentItemSet>> finalFrequentItemSets = new ArrayList<>();
		ArrayList<FrequentItemSet> currentLargeSet = prepareOneItemSet(items, dataSet, minSupport);
		if(currentLargeSet.size() > 0){
			finalFrequentItemSets.add(currentLargeSet);
			while (currentLargeSet.size() > 0) {
				int[][] candidateItemSets = selfJoinAndPrune(convertArrayListToArray(currentLargeSet), dataSet, minSupport);
				currentLargeSet = getFrequentItemSet(candidateItemSets, dataSet, minSupport);
				if(currentLargeSet.size() == 0)
					break;
				finalFrequentItemSets.add(currentLargeSet);
			}
		}
		return finalFrequentItemSets;
	}
	
	public int[][] convertArrayListToArray(ArrayList<FrequentItemSet> itemSet) {
		
		if(itemSet != null){
			if(itemSet.size() == 0){
				return new int[0][];
			}else {
				int[][] output = new int[itemSet.size()][];
				for (int i = 0; i < itemSet.size(); i++) {
					output[i] = itemSet.get(i).itemSet;
				}
				return output;
			}
		}else {
			return new int[0][];
		}
	}
	
	public int[][] selfJoinAndPrune(int[][] data,int[][] dataSet,int minSupport){
		if(data != null && dataSet != null && minSupport>0){
			if(data.length == 0 || dataSet.length == 0){
				return new int[0][];
			}else {
				ArrayList<int[]> output = new ArrayList<>();
				for (int i = 0; i < data.length; i++) {
					for (int j = i+1; j < data.length; j++) {
						if(couldBeJoined(data[i], data[j])){
							int[] temp = microJoin(data[i], data[j]);
							if(!shouldBePruned(temp, dataSet, minSupport)){
								output.add(temp);	
							}
						}
					}
				}
				
				int[][] out = new int[output.size()][];
				for (int j = 0; j < output.size(); j++) {
					out[j] = new int[output.get(j).length];
					out[j] = output.get(j);
				}
				return out;
			}
		}else {
			return new int[0][];
		}
	}
	
	public int[] microJoin(int[] first,int[] second){
		if(first.length == 1 || second.length == 1){
			int[] temp = new int[2];
			temp[0] = first[0];
			temp[1] = second[0];
			return temp;
		}else {
			int lastIndex = first.length - 1;
			int[] temp = new int[first.length + 1];
			for (int i = 0; i < first.length; i++) {
				temp[i] = first[i];
			}
			temp[first.length] = second[lastIndex];
			return temp;
		}
	}
	
	public boolean couldBeJoined(int[] first,int[] second){
		if(first.length == 1 || second.length == 1)
			return true;
		else{
			int lastIndex = first.length - 1;
			boolean isFirstPartSame = true;
			for (int i = 0; i < lastIndex; i++) {
				if(first[i] != second[i]){
					isFirstPartSame = false;
					break;
				}
			}
			if(isFirstPartSame){
				if(first[lastIndex] != second[lastIndex])
					return true;
				else
					return false;
			}else
				return false;
		}
	}
	
	public boolean shouldBePruned(int[] record,int[][] dataSet,int minSupport){
		
		int[][] subSets = getAllSubSets(record);
		for (int[] subRecord : subSets) {
			int count = getOccuranceCount(subRecord, dataSet);
			if(count < minSupport){
				return true;
			}
		}
		return false;
	}
	
	public int[][] getAllSubSets(int[] record){
		
		if(record.length == 2){
			int[][] output = new int[2][];
			int[] firstOne = new int[1];
			int[] secondOne = new int[1];
			firstOne[0] = record[0];
			secondOne[0] = record[1];
			output[0] = firstOne;
			output[1] = secondOne;
			return output;
		}else {
			int[][] output = new int[record.length][record.length -1];
			int[] secondSideRecord = new int[record.length - 1];
			for (int i = 0; i < secondSideRecord.length; i++) {
				secondSideRecord[i] = record[i+1];
			}
			int[][] tempItemSet = getAllSubSets(secondSideRecord);
			for (int j = 0; j < record.length - 1; j++) {
				int[] tempRecord = new int[record.length - 1];
				tempRecord[0] = record[0];
				for (int k = 0; k < tempRecord.length -1; k++) {
					tempRecord[k+1] = tempItemSet[j][k];
				}
				output[j] = tempRecord;
			}
			output[record.length - 1] = secondSideRecord;
			return output;
		}
	}
	
	public ArrayList<FrequentItemSet> prepareOneItemSet(int[] items,int[][] dataSet,int minSupport) {
		
		if(items != null && dataSet != null && minSupport > 0){
			if(items.length == 0 || dataSet.length == 0){
				return new ArrayList<>();
			}else {
				ArrayList<FrequentItemSet> output = new ArrayList<>();
				for (int i=0; i<items.length ; i++) {
					int[] temp = new int[1];
					temp[0] = items[i];
					int count = getOccuranceCount(temp, dataSet);
					if(count >= minSupport){
						FrequentItemSet frequentItemSet = new FrequentItemSet();
						frequentItemSet.itemSet = temp;
						frequentItemSet.count = count;
						output.add(frequentItemSet);
					}
				}
				return output;
			}
		}else {
			return new ArrayList<>();
		}
	}
	
	public ArrayList<FrequentItemSet> getFrequentItemSet(int[][] itemSets,int[][] dataSet,int minSupport) {
		
		if(itemSets != null && dataSet != null && minSupport > 0){
			if(itemSets.length == 0 || dataSet.length == 0)
				return new ArrayList<>();
			else {
				ArrayList<FrequentItemSet> output = new ArrayList<>();
				for (int[] record : itemSets) {
					int count = getOccuranceCount(record, dataSet);
					if(count >= minSupport){
						FrequentItemSet frequentItemSet = new FrequentItemSet();
						frequentItemSet.itemSet = record;
						frequentItemSet.count = count;
						output.add(frequentItemSet);
					}
				}
				return output;
			}
		}else {
			return new ArrayList<>();
		}
		
	}
	
	public int getOccuranceCount(int[] record,int[][] dataSet){
		
		int count = 0;
		for (int[] data : dataSet) {
			boolean consistence = true;
			for (int i = 0; i < record.length; i++) {
				data = new SortInteger().sort(data);
				if(!new BinarySearch().binarySearch(data, data.length, record[i])){
					consistence = false;
					break;
				}
			}
			if(consistence)
				count++;
		}
		
		return count;
	}

}
