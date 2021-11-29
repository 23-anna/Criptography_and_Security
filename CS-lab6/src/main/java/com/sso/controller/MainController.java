package com.sso.controller;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import import java.util.List;

@RestController
public class MainController {

    @GetMapping("/")
    public String main(Authentication authentication){
        String authenticationData = authentication.toString();

        List<String, String> htmlBuilder = new List<>;
        htmlBuilder.put("message", authenticationData);

        return "index";
    }
}
