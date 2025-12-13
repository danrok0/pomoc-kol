package com.stockmarket.logic;

import com.stockmarket.domain.*;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class PortfolioTest {

    @Test
    void polymorphismTest_assetsWithSameBasePriceShouldHaveDifferentRealValues() {
        // given: 3 różne aktywa o tej samej cenie 100 PLN
        BigDecimal price = new BigDecimal("100.00");
        Share share = new Share("S", price);             // 100 - 5 = 95
        Commodity commodity = new Commodity("C", price, new BigDecimal("10")); // 100 - 10 = 90
        Currency currency = new Currency("M", price, new BigDecimal("1"));     // 99

        // when
        BigDecimal v1 = share.calculateRealValue(1);
        BigDecimal v2 = commodity.calculateRealValue(1);
        BigDecimal v3 = currency.calculateRealValue(1);

        // then: Każde musi dać inny wynik
        assertThat(v1).isNotEqualByComparingTo(v2);
        assertThat(v2).isNotEqualByComparingTo(v3);
        assertThat(v1).isNotEqualByComparingTo(v3);
    }

    @Test
    void shouldThrowExceptionWhenBuyingTooMuch() {
        // given: portfel z 100 PLN
        Portfolio p = new Portfolio(new BigDecimal("100.00"));
        Share expensive = new Share("Drogie", new BigDecimal("200.00"));

        // then: próba zakupu musi rzucić wyjątek
        assertThatThrownBy(() -> p.addAsset(expensive, 1))
                .isInstanceOf(IllegalStateException.class);
    }
}

