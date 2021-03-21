extern crate clap;
extern crate rpassword;
extern crate aes_gcm_siv;
extern crate base64;
extern crate rand;
use clap::{Arg, App};
use aes_gcm_siv::Aes256GcmSiv;
use aes_gcm_siv::aead::{Aead, NewAead, generic_array::GenericArray};
use base64::{encode, decode};
use rand::{distributions::Alphanumeric, Rng};

fn encrypt_file(pass: &str, file: &str) {
    println!("{}", pass);
    let key = GenericArray::from_slice(pass.as_bytes());
    let cipher = Aes256GcmSiv::new(&key);

    // generate nonce
    let rstr: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(12) // 96 bits
        .map(char::from)
        .collect();
    println!("Random Nonce: {}", rstr);
    println!("Password (remove): {}", pass); // for testing
    // let nonce = GenericArray::from_slice(rstr.as_bytes());

    // get key
    // let key = GenericArray::clone_from_slice(pass.as_bytes());
    // let cipher = Aes256GcmSiv::new(key);

    // let ciphertext = cipher.encrypt(nonce, encode(file).as_bytes().as_ref()).expect("Failed to encrypt!");

}

fn decrypt_file() {
}

fn main() {
    // get opts
    let matches = App::new("File Crypter")
        .version("0.1.0")
        .author("Enya Yang <https://www.github.com/cdohara>")
        .about("Encrypts a selected file using AES256-GCM-SIV")
        .arg(Arg::new("FILE")
            .short('f')
            .long("file")
            .takes_value(true)
            .required(true)
            .about("File to encrypt"))
        .arg(Arg::new("decrypt")
            .short('d')
            .long("decrypt")
            .about("Decrypts file"))
        .get_matches();
    
    let file = matches.value_of("FILE").unwrap();
    let encrypt: bool = !matches.is_present("decrypt");

    // print file information and status information
    println!("File: {}", file);
    print!("Mode: ");
    if encrypt {
        println!("Encryption")
    } else {
        println!("Decryption")
    }

    // get password
    let pass = rpassword::read_password_from_tty(Some("Enter Password: ")).unwrap();

    if encrypt {
        encrypt_file(&pass, file);
    } else {
        decrypt_file();
    }


}
