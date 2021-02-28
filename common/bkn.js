function getbkn(skey) {
    var e = skey;
    if (e) {
        for (var t = 5381, n = 0, r = e.length; n < r; ++n) t += (t << 5) + e.charAt(n).charCodeAt();
        return this.CSRFToken = 2147483647 & t
    }
}

function ptqrtoken(t) {
    for (var e = 0, i = 0, n = t.length; i < n; ++i) e += (e << 5) + t.charCodeAt(i);
    return 2147483647 & e
}