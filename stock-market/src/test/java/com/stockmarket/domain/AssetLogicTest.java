package com.stockmarket.domain;

import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.assertj.core.api.Assertions.assertThat;

class AssetLogicTest {

    @Test
    void shareShouldReduceValueByHandlingFee() {
        // Akcja warta 100, opłata 5.
        // 1 sztuka powinna być warta 95.
        Share share = new Share("TestShare", new BigDecimal("100.00"));
        assertThat(share.calculateRealValue(1))
                .isEqualByComparingTo(new BigDecimal("95.00"));
    }

    @Test
    void commodityShouldReduceValueByStorageCost() {
        // Surowiec 100, koszt mag. 10.
        // 2 sztuki: (100*2) - (10*2) = 200 - 20 = 180.
        Commodity gold = new Commodity("Gold", new BigDecimal("100.00"), new BigDecimal("10.00"));
        assertThat(gold.calculateRealValue(2))
                .isEqualByComparingTo(new BigDecimal("180.00"));
    }

    @Test
    void currencyShouldReduceValueBySpread() {
        // Waluta 5.00, spread 0.20.
        // Cena Bid = 4.80.
        // 100 sztuk = 480.00.
        Currency euro = new Currency("EUR", new BigDecimal("5.00"), new BigDecimal("0.20"));
        assertThat(euro.calculateRealValue(100))
                .isEqualByComparingTo(new BigDecimal("480.00"));
    }
}