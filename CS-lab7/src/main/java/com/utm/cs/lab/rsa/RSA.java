package com.utm.cs.lab.rsa;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;


public class RSA implements IRSA {

    private final static BigInteger ONE = new BigInteger("1");
    private BigInteger privateKey;
    private BigInteger e;
    private BigInteger n;
    private BigInteger p;
    private BigInteger q;
    private final BigInteger phi;

    RSA(BigInteger p, BigInteger q, BigInteger e) {

        phi = (p.subtract(ONE)).multiply(q.subtract(ONE));
        this.e = e;
        this.p = p;
        this.q = q;
        n = p.multiply(q);
        privateKey = e.modInverse(phi);
    }

    @Override
    public BigInteger encrypt(BigInteger bigInteger) {
        if (isModulusSmallerThanMessage(bigInteger)) {
            throw new IllegalArgumentException("Could not encrypt - message bytes are greater than modulus");
        }
        return bigInteger.modPow(e, n);
    }

    public List<BigInteger> encryptMessage(final String message) {
        List<BigInteger> toEncrypt = new ArrayList<BigInteger>();
        BigInteger messageBytes = new BigInteger(message.getBytes());
        if (isModulusSmallerThanMessage(messageBytes)) {
            toEncrypt =
                    getValidEncryptionBlocks(Utils.splitMessages(new ArrayList<String>() {
                {
                    add(message);
                }
            }));
        } else {
            toEncrypt.add((messageBytes));
        }
        List<BigInteger> encrypted = new ArrayList<BigInteger>();
        for (BigInteger bigInteger : toEncrypt) {
            encrypted.add(this.encrypt(bigInteger));
        }
        return encrypted;
    }



    @Override
    public BigInteger decrypt(BigInteger encrypted) {
        return encrypted.modPow(privateKey, n);
    }

    public List<BigInteger> decrypt(List<BigInteger> encryption) {
        List<BigInteger> decryption = new ArrayList<BigInteger>();
        for (BigInteger bigInteger : encryption) {
            decryption.add(this.decrypt(bigInteger));
        }
        return decryption;
    }


    private List<BigInteger> getValidEncryptionBlocks(List<String> messages) {
        List<BigInteger> validBlocks = new ArrayList<BigInteger>();
        BigInteger messageBytes = new BigInteger(messages.get(0).getBytes());
        if (!isModulusSmallerThanMessage(messageBytes)) {
            for (String msg : messages) {
                validBlocks.add(new BigInteger(msg.getBytes()));
            }
            return validBlocks;
        } else {
            return getValidEncryptionBlocks(Utils.splitMessages(messages));
        }

    }

    
    public List<BigInteger> messageToDecimal(final String message) {
        List<BigInteger> toDecimal = new ArrayList<BigInteger>();
        BigInteger messageBytes = new BigInteger(message.getBytes());
        if (isModulusSmallerThanMessage(messageBytes)) {
            toDecimal = getValidEncryptionBlocks(Utils.splitMessages(new ArrayList<String>() {
                {
                    add(message);
                }
            }));
        } else {
            toDecimal.add((messageBytes));
        }
        List<BigInteger> decimal = new ArrayList<BigInteger>();
        for (BigInteger bigInteger : toDecimal) {
            decimal.add(bigInteger);
        }
        return decimal;
    }


    private boolean isModulusSmallerThanMessage(BigInteger messageBytes) {
        return n.compareTo(messageBytes) == -1;
    }

    @Override
    public String toString() {
        String s = "";
        s += "p                     = " + p + "\n";
        s += "q                     = " + q + "\n";
        s += "e                     = " + e + "\n";
        s += "private               = " + privateKey + "\n";
        s += "n                     = " + n;
        return s;
    }
}