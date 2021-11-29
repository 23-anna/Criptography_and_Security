package com.utm.cs.lab.rsa;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

public class Encryption {

    private final static BigInteger p = new BigInteger("98178641836801910294873665182392109312435362778190");
    private final static BigInteger q = new BigInteger("39173498322104834701816154367283784937623721927301");
    private final static BigInteger e = new BigInteger("12389484680094000054847388767836762647858783212438");

    public static String encrypt(String message) {

        IRSA rsa = new RSA(p, q, e);

        System.out.println(rsa);

        List<BigInteger> encryption;
        List<BigInteger> signed;
        List<BigInteger> decimalMessage;

            encryption = rsa.encryptMessage(message);
            decimalMessage = rsa.messageToDecimal(message);

        List<BigInteger> decrypt = rsa.decrypt(encryption);
        System.out.println();
        System.out.println("message(plain text)   = " + Utils.bigIntToString(decimalMessage));
        System.out.println("message(decimal)      = " + Utils.bigIntSum(decimalMessage));
        System.out.println("encripted(decimal)    = " + Utils.bigIntSum(encryption));
        System.out.println("decrypted(plain text) = " + Utils.bigIntToString(decrypt));
        System.out.println("decrypted(decimal)    = " + Utils.bigIntSum(decrypt));

    return Utils.bigIntSum(encryption);
    }

    public static String decrypt(String encMessage){

        IRSA rsa = new RSA(p, q, e);

        List<BigInteger> encrypted = new ArrayList<BigInteger>();
        encrypted.add(new BigInteger(encMessage));
        List<BigInteger> decrypt = rsa.decrypt(encrypted);
        return Utils.bigIntToString(decrypt);
    }
}



