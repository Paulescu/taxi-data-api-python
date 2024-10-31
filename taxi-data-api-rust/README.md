# Steps

- [ ] Create Rust project structure
- [ ] Don't forget Rust analyzer
- [ ] Add actix-web
- [ ] Create the HttpServer
- [ ] Add /health endpoint

- [ ] Easy error handling with anyhow

- [ ] Set port from env variable
- [ ] Add middleware for logging
- [ ] Add /trips endpoint
- [ ] Create another module backend.rs with the get_trips function
- [ ] Implement the get_trips function 


## Notes

`unwrap()` extracts the value from an `Option` or a `Result` type, but it does that in
a dangerous way. It will Panic and crash the program if the valueis None or Err.

Alternatives:
* `expect()` with a meaningfull message
* Patter matching with `match`
* `unwrap_or()` to provide a default value
* `ok_or()` to convert to a Result