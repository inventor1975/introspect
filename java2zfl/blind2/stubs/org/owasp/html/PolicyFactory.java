package org.owasp.html; public final class PolicyFactory { public String sanitize(String html){return html;} public PolicyFactory and(PolicyFactory f){return this;} }
