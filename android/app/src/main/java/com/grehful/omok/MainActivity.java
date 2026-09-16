package com.grehful.omok;

import android.os.Bundle;
import android.webkit.WebSettings;

import androidx.webkit.WebSettingsCompat;
import androidx.webkit.WebViewFeature;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 시스템이 다크 모드면 WebView 안의 prefers-color-scheme 도 dark 로 보이게 한다.
        if (WebViewFeature.isFeatureSupported(WebViewFeature.ALGORITHMIC_DARKENING)) {
            WebSettings settings = getBridge().getWebView().getSettings();
            WebSettingsCompat.setAlgorithmicDarkeningAllowed(settings, true);
        }
    }
}
