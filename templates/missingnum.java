import java.util.*;

public class Main
{
	public static void main(String[] args) {
		Scanner sc=new Scanner(System.in);
		System.out.println("Enter n value");
		int n=sc.nextInt();
		int arr[]=new int[n];
		System.out.println("Enter n-1 values");
		for(int i=0;i<=n-2;i++){
		    arr[i]=sc.nextInt();
		}
		int b=0;
		int a=0;
		for(int i=0;i<=n;i++){
		    a=a+i;
		}
		for(int i=0;i<=n-2;i++){
		    b=b+arr[i];
		}
		int x=a-b;
		System.out.println("Missing number"+x);
	}
}
