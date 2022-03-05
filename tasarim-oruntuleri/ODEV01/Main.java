public class Main {
    public static void main(String args[]) {
    }
}

interface Ucabilir {
    public void uc();
}

interface Yuruyebilir {
    public void yuru();
}

abstract class Kus {
    public  Kus(int yas, String isim) {
        this.yas = yas;
        this.isim = isim;
    }

    protected int yas = 0;
    protected String isim = "kuş";

    public String getIsim() {
        return isim;
    }

    public int getYas() {
        return yas;
    }
    
    public void setIsim(String isim) {
        this.isim = isim;
    }
    
    public void setYas(int yas) {
        this.yas = yas;
    }

    final public void baseinfo() {
        System.out.println("Kus ana sınıfı");
    }

    static public void info() {
        System.out.println("Kuş sınıfı statik metod");
    }

    public void yazIsım() {
        System.out.println("İsim:" + this.isim);
    }

    public void yazYas() {
        System.out.println("Yas:" + this.isim);
    }
}

class Baykus extends Kus implements Ucabilir, Yuruyebilir {
    public Baykus(int yas, String isim) {
        super(yas, isim);
    }

    @Override
    public void uc() {
        System.out.println("Baykus sınıfına ait 'uc' metodu");
    }

    @Override
    public void yuru() {
        System.out.println("Baykus sınıfına ait 'yuru' metodu");
    }

    /**
     * Java derleyicisi baseinfo fonksiyonunun override edilmesine izin vermez
     */
    // @Override
    // public void baseinfo() {
    //     System.out.println("method of Class B");
    // }
}

class Guvercin extends Kus implements Ucabilir, Yuruyebilir {
    public Guvercin(int yas, String isim) {
        super(yas, isim);
    }

    @Override
    public void uc() {
        System.out.println("Guvercin sınıfına ait 'uc' metodu");
    }

    @Override
    public void yuru() {
        System.out.println("Guvercin sınıfına ait 'yuru' metodu");
    }
}

class DeveKusu extends Kus implements Yuruyebilir {
    public DeveKusu(int yas, String isim) {
        super(yas, isim);
    }

    @Override
    public void yuru() {
        System.out.println("DeveKusu sınıfına 'yuru' metodu");
    }
}
