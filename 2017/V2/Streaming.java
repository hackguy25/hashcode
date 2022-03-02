import java.util.*;

public class Streaming {
	
	//	V2: upoštevanje latenc serverjev pri weightanju
	
	public static void main (String [] args) {
		
		Scanner sc = new Scanner(System.in);
		
		int v = sc.nextInt();
		int e = sc.nextInt();
		int r = sc.nextInt();
		int c = sc.nextInt();
		int x = sc.nextInt();
		
		int[] velikosti = new int[v];
		int[] zasedenosti = new int[c];
		
		for (int i = 0; i < v; i++) {
			velikosti[i] = sc.nextInt();
		}
		
		int[] centerZamiki = new int[e];
		int[][][] cacheZamiki = new int[e][c][2];
		
		for (int i = 0; i < e; i++) {
			
			centerZamiki[i] = sc.nextInt();
			
			int k = sc.nextInt();
			cacheZamiki[i] = new int[k][2];
			
			for (int j = 0; j < k; j++) {
				
				cacheZamiki[i][j][0] = sc.nextInt();
				cacheZamiki[i][j][1] = sc.nextInt();
			}
		}
		
		int[][] req = new int[r][3];
		
		for (int i = 0; i < r; i++) {
			
			req[i][0] = sc.nextInt();
			req[i][1] = sc.nextInt();
			req[i][2] = sc.nextInt();
		}
		
		boolean[][] videi = new boolean[c][v];
		
		/*	No, pa začnimo! */
		
		//	Razvrščanje zamikov cachejev po latencah
		
		for (int[][] trenutniEP : cacheZamiki) {
			for (int i = 0; i < trenutniEP.length - 1; i++) {
				
				int minIdx = i;
				int minZamik = trenutniEP[i][1];
				
				for (int j = i + 1; j < trenutniEP.length; j++) {
					
					if (trenutniEP[j][1] < minZamik) {
						minIdx = j;
						minZamik = trenutniEP[j][1];
					}
				}
				
				int[] temp = trenutniEP[i];
				trenutniEP[i] = trenutniEP[minIdx];
				trenutniEP[minIdx] = temp;
			}
		}
		
		//	Razvrščanje request skupine z največjim n * deltaZamika * (deltaZamika - zamikCache)

		for (int i = 0; i < r - 1; i++) {
			
			int maxIdx = i;
			int idxBestServerja = -1;
			int latencaBestServerja = centerZamiki[req[i][1]];
			
			for (int j = 0; j < cacheZamiki[req[i][1]].length; j++) {
				if (cacheZamiki[req[i][1]][j][1] < latencaBestServerja) {
					
					idxBestServerja = j;
					latencaBestServerja = cacheZamiki[req[i][1]][j][1];
				}
			}
			
			int maxWeight = req[i][2] * centerZamiki[req[i][1]] * (centerZamiki[req[i][1]] - latencaBestServerja);
			
			for (int j = i + 1; j < r; j++) {
				
				idxBestServerja = -1;
				latencaBestServerja = centerZamiki[req[j][1]];
				
				for (int k = 0; k < cacheZamiki[req[j][1]].length; k++) {
					if (cacheZamiki[req[j][1]][k][1] < latencaBestServerja) {
						
						idxBestServerja = k;
						latencaBestServerja = cacheZamiki[req[j][1]][k][1];
					}
				}
				
				if (maxWeight < req[j][2] * centerZamiki[req[j][1]] * (centerZamiki[req[j][1]] - latencaBestServerja)) {
					maxIdx = j;
					maxWeight = req[j][2] * centerZamiki[req[j][1]] * (centerZamiki[req[j][1]] - latencaBestServerja);
				}
			}
			
			int[] temp = req[i];
			req[i] = req[maxIdx];
			req[maxIdx] = temp;
			
			if (idxBestServerja != -1 && zasedenosti[cacheZamiki[req[i][1]][idxBestServerja][0]] + velikosti[req[i][0]] <= x) {
				
				zasedenosti[cacheZamiki[req[i][1]][idxBestServerja][0]] += velikosti[req[i][0]];
				videi[cacheZamiki[req[i][1]][idxBestServerja][0]][req[i][0]] = true;
				break;
			}
		}
		
		/*
		for (int i = 0; i < e; i++) {
			for (int j = 0; j < cacheZamiki[i].length; j++) {
				
				System.out.println(cacheZamiki[i][j][0] + " " + cacheZamiki[i][j][1]);
			}
			System.out.println();
		}
		*/
		
		int vrstic = 0;
		boolean[] smoPolnili = new boolean[c];
		
		for (int i = 0; i < c; i++) {
			for (int j = 0; j < v; j++) {
				if (videi[i][j]) {
					
					smoPolnili[i] = true;
					vrstic++;
					break;
				}
			}
		}
		
		System.out.print(vrstic);
		
		for (int i = 0; i < c; i++) {
			if (smoPolnili[i]) {
				
				System.out.println();
				System.out.print(i);
				
				for (int j = 0; j < v; j++) {
					if (videi[i][j]) {
						
						System.out.print(" " + j);
					}
				}
			}
		}
	}
}