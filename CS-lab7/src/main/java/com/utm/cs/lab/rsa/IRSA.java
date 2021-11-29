
package com.utm.cs.lab.rsa;

import java.io.Serializable;
import java.math.BigInteger;
import java.util.List;

public interface IRSA extends Serializable {

    BigInteger encrypt(BigInteger bigInteger);

    List<BigInteger> encryptMessage(final String message);

    BigInteger decrypt(BigInteger encrypted);

    List<BigInteger> decrypt(List<BigInteger> encryption);

    List<BigInteger> messageToDecimal(final String message);

}
