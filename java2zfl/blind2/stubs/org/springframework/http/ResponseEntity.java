package org.springframework.http; public class ResponseEntity<T> {
 public ResponseEntity(T body, HttpStatus s){} public ResponseEntity(HttpStatus s){}
 public static <T> ResponseEntity<T> ok(T body){return null;} public static BodyBuilder ok(){return null;} public static BodyBuilder badRequest(){return null;} public static BodyBuilder status(HttpStatus s){return null;}
 public T getBody(){return null;}
 public interface BodyBuilder { BodyBuilder contentType(MediaType m); BodyBuilder header(String n, String... v); <T> ResponseEntity<T> body(T b); <T> ResponseEntity<T> build(); } }
