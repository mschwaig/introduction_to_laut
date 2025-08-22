# An introduction to the laut signature format

This is my talk about https://github.com/mschwaig/laut at the the [NixOS User Group Austria](https://nixos.at).

Laut is a proposed new signature format for Nix.
Since this is a pretty technical topic, we will try to look at it from the user perspective, and I will try to show concrete things on the command line.
Let's start with the base line:

### Looking up a signature based on the legacy signature format

We're just calling the current format legacy here, let's see what that does. There is a glossary at https://github.com/mschwaig/laut.

Let's find the version of `nixpkgs` that laut uses right now, so we can look up things in the caches from its VM tests later:

```
mschwaig@mutalisk ~/g/laut (main)> nix flake metadata --json | jq -r '.locks.nodes.nixpkgs_2.locked.rev'
979daf34c8cacebcd917d540070b52a3c2b9b16e
```

... and go look at that version of the hello derivation:

```
mschwaig@mutalisk ~/g/laut (main)> nix derivation show nixpkgs/979daf34c8cacebcd917d540070b52a3c2b9b16e#hello
{
  "/nix/store/iqbwkm8mjjjlmw6x6ry9rhzin2cp9372-hello-2.12.1.drv": {
    "args": [
      "-e",
      "/nix/store/vj1c3wf9c11a0qs6p3ymfvrnsdgsdcbq-source-stdenv.sh",
      "/nix/store/shkw4qm9qcw5sc5n1k5jznc83ny02r39-default-builder.sh"
    ],
    "builder": "/nix/store/9nw8b61s8lfdn8fkabxhbz0s775gjhbr-bash-5.2p37/bin/bash",
    "env": {
      "__structuredAttrs": "",
      "buildInputs": "",
      "builder": "/nix/store/9nw8b61s8lfdn8fkabxhbz0s775gjhbr-bash-5.2p37/bin/bash",
      "cmakeFlags": "",
      "configureFlags": "",
      "depsBuildBuild": "",
      "depsBuildBuildPropagated": "",
      "depsBuildTarget": "",
      "depsBuildTargetPropagated": "",
      "depsHostHost": "",
      "depsHostHostPropagated": "",
      "depsTargetTarget": "",
      "depsTargetTargetPropagated": "",
      "doCheck": "1",
      "doInstallCheck": "1",
      "mesonFlags": "",
      "name": "hello-2.12.1",
      "nativeBuildInputs": "/nix/store/bx6flpzk0dcs04ncsxxcgg849xaf93z6-version-check-hook",
      "out": "/nix/store/9bwryidal9q3g91cjm6xschfn4ikd82q-hello-2.12.1",
      "outputs": "out",
      "patches": "",
      "pname": "hello",
      "postInstallCheck": "stat \"${!outputBin}/bin/hello\"\n",
      "propagatedBuildInputs": "",
      "propagatedNativeBuildInputs": "",
      "src": "/nix/store/pa10z4ngm0g83kx9mssrqzz30s84vq7k-hello-2.12.1.tar.gz",
      "stdenv": "/nix/store/plgd01gl1wvxyaxw2iafcr739s5icrsf-stdenv-linux",
      "strictDeps": "",
      "system": "x86_64-linux",
      "version": "2.12.1"
    },
    "inputDrvs": {
      "/nix/store/g6xv14j4bcdy1aj0srgyymrmanyp1zk4-version-check-hook.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      },
      "/nix/store/kgzss88arlqr66v79xg5azs7cwcrn4ix-hello-2.12.1.tar.gz.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      },
      "/nix/store/lrf9kbhlaf5mkvnlf3zr9wzvk7c2z72l-bash-5.2p37.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      },
      "/nix/store/y4zk72najykpa9lbjjj7gcvqxwncq8xb-stdenv-linux.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      }
    },
    "inputSrcs": [
      "/nix/store/shkw4qm9qcw5sc5n1k5jznc83ny02r39-default-builder.sh",
      "/nix/store/vj1c3wf9c11a0qs6p3ymfvrnsdgsdcbq-source-stdenv.sh"
    ],
    "name": "hello-2.12.1",
    "outputs": {
      "out": {
        "path": "/nix/store/9bwryidal9q3g91cjm6xschfn4ikd82q-hello-2.12.1"
      }
    },
    "system": "x86_64-linux"
  }
}
```

The `inputSrcs` are leaves at the edge of the dependency tree. Their store paths are based on a hash of their contents. We took them in as content, think source code or some opaque blob checked into the repo.

The `inputDrvs` are derivations, so they are nodes within the dependency tree, and their address is based on the hash of the derivation that builds them, not the content. So it's a hash of the build recipe.
Same is true for the output path of this derivation itself.

Now we go look this up on https://cache.nixos.org using the hash from the output store path:

```
curl https://cache.nixos.org/wvfhs8k86740b7j3h1iss94z7cb0ggj1.narinfo
StorePath: /nix/store/wvfhs8k86740b7j3h1iss94z7cb0ggj1-hello-2.12.2
URL: nar/1p5mlq8w84jhp79pgykhgp7xi2lw5mijcf42g9d0x342zz489xv2.nar.xz
Compression: xz
FileHash: sha256:1p5mlq8w84jhp79pgykhgp7xi2lw5mijcf42g9d0x342zz489xv2
FileSize: 57500
NarHash: sha256:1q27ixp15f8ggr11gjfgqql5s10iwv9gnh3hqgwdwrrxwk0kc0ii
NarSize: 274392
References: lmn7lwydprqibdkghw7wgcn21yhllz13-glibc-2.40-66 wvfhs8k86740b7j3h1iss94z7cb0ggj1-hello-2.12.2
Deriver: 5g60vyp4cbgwl12pav5apyi571smp62s-hello-2.12.2.drv
Sig: cache.nixos.org-1:qzsDAeq7dRyXpCyBtj4t+yZjaBFQcNf+Tp0XMVEm8/p1XS8GtA1cSYngx6fI07ib61ZNd0A8tWypIC0KxHs4AA==
```

The code to verify this signature is in https://github.com/NixOS/nix/blob/e3febfcd532adb23ca05ac465a2b907d6f1a3529/src/libstore/path-info.cc#L25
`
but I wrote a small python script to verify it instead, so we can do it standalone: [verify_nix_signature.py](verify_nix_signature.py)


Mainly the signature associates
1. a hash that depends on all the inputs: `StorePath`
2. with a hash of the output `NarHash`

A few key problems:
1. We don't know what was actually stored at the input store paths, because the paths inside `inputDrvs` are input-addressed (IA) not content-addressed (CA).
  - We have to trust the signer with what they put there, which is based on THEIR trust relationships, not MINE. This is pretty universal in software distribution, so people just accept it.
2. We don't even know WHO originally did the build. We have to make a guess based on trust and how the infra in question is supposed to work.
3. The format itself is based on a closed set of datapoints, unless you smuggle things in the padding or name portion.
4. outputs have underspecified dependencies as well
5. it links things at the output path level instead of the derivation level

### How CA derivations solve the problem with `inputDrvs`

With the store path of the flake from earlier, we can get the CA version of hello:
```
mschwaig@mutalisk ~/g/laut_nixos_at> nix derivation show -f /nix/store/pxnx7dbr0pz3qpgw2r315wdbb00afdw7-source hello --arg config '{ contentAddressedByDefault = true; }'
warning: Nix search path entry '/nix/var/nix/profiles/per-user/root/channels' does not exist, ignoring
{
  "/nix/store/hl7xw502hl7dddq0130m20frygzlp4s4-hello-2.12.2.drv": {
    "args": [
      "-e",
      "/nix/store/vj1c3wf9c11a0qs6p3ymfvrnsdgsdcbq-source-stdenv.sh",
      "/nix/store/shkw4qm9qcw5sc5n1k5jznc83ny02r39-default-builder.sh"
    ],
    "builder": "/0g27hf0b3gnw6aiiq3ghf4g2g405m070imh8mckp7318f6vn08yl/bin/bash",
    "env": {
      "NIX_MAIN_PROGRAM": "hello",
      "__structuredAttrs": "",
      "buildInputs": "",
      "builder": "/0g27hf0b3gnw6aiiq3ghf4g2g405m070imh8mckp7318f6vn08yl/bin/bash",
      "cmakeFlags": "",
      "configureFlags": "",
      "depsBuildBuild": "",
      "depsBuildBuildPropagated": "",
      "depsBuildTarget": "",
      "depsBuildTargetPropagated": "",
      "depsHostHost": "",
      "depsHostHostPropagated": "",
      "depsTargetTarget": "",
      "depsTargetTargetPropagated": "",
      "doCheck": "1",
      "doInstallCheck": "1",
      "mesonFlags": "",
      "name": "hello-2.12.2",
      "nativeBuildInputs": "/13mspq6sjcc4q770f7h8l8mm25qs8hsr6b5fba6qrrhz6dwqwya3",
      "out": "/1rz4g4znpzjwh1xymhjpm42vipw92pr73vdgl6xs1hycac8kf2n9",
      "outputHashAlgo": "sha256",
      "outputHashMode": "recursive",
      "outputs": "out",
      "patches": "",
      "pname": "hello",
      "postInstallCheck": "stat \"${!outputBin}/bin/hello\"\n",
      "propagatedBuildInputs": "",
      "propagatedNativeBuildInputs": "",
      "src": "/nix/store/dw402azxjrgrzrk6j0p66wkqrab5mwgw-hello-2.12.2.tar.gz",
      "stdenv": "/0aq6b97i80xmm88h9ls31n9ppwdgzdgbvsj3x51lkxnnc1fiy01l",
      "strictDeps": "",
      "system": "x86_64-linux",
      "version": "2.12.2"
    },
    "inputDrvs": {
      "/nix/store/25mhy34n3x4cmwh7pq4gbpn844lcdmkw-bash-5.3p0.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      },
      "/nix/store/6zcv32qm212km6qyysg4qpa60jayb2ca-hello-2.12.2.tar.gz.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      },
      "/nix/store/d9yj9nrm9j2yl081gbj56pmdf8byzgwa-version-check-hook.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      },
      "/nix/store/hjqgzp59v57ra1bcf7ywdnhx092bx8h9-stdenv-linux.drv": {
        "dynamicOutputs": {},
        "outputs": [
          "out"
        ]
      }
    },
    "inputSrcs": [
      "/nix/store/shkw4qm9qcw5sc5n1k5jznc83ny02r39-default-builder.sh",
      "/nix/store/vj1c3wf9c11a0qs6p3ymfvrnsdgsdcbq-source-stdenv.sh"
    ],
    "name": "hello-2.12.2",
    "outputs": {
      "out": {
        "hashAlgo": "sha256",
        "method": "nar"
      }
    },
    "system": "x86_64-linux"
  }
}
```

The main differences between this and the IA version are
* there are no output paths (because they are CA, so unknown in advance)
* there are upstream placeholders like `/0aq6b97i80xmm88h9ls31n9ppwdgzdgbvsj3x51lkxnnc1fiy01l` (a hack, so we can refer to things that have no path yet outside of `inputDrvs`) :(

So this does not look like it solves our problem, but
* there exists a resolved version of that derivation (RFC 61 calls them basic derivations)

This one is a pain to obtain, because we need to build all the dependencies of hello first, but it it addresses the 1st issue we mentioned above.

I'm pulling this one out of the `input.debug` section of a laut signature at `tests/data/lookup_by_name/builderA_bcda8d54470fea3b.json`, so the `rdrv_path` line should be deleted and it's value should go in the place of the "rdrv_json_preimage" key:

```
  "rdrv_path": "/nix/store/7gsw68f2iawn9q8vv04zh9xql14268pw-hello-2.12.1.drv",
  "rdrv_json_preimage": {
    "args": [
      "-e",
      "/nix/store/vj1c3wf9c11a0qs6p3ymfvrnsdgsdcbq-source-stdenv.sh",
      "/nix/store/shkw4qm9qcw5sc5n1k5jznc83ny02r39-default-builder.sh"
    ],
    "builder": "/nix/store/an6si0s9azgz2wavyrvvlx8g76k4zifv-bash-5.2p37/bin/bash",
    "env": {
      "__structuredAttrs": "",
      "buildInputs": "",
      "builder": "/nix/store/an6si0s9azgz2wavyrvvlx8g76k4zifv-bash-5.2p37/bin/bash",
      "cmakeFlags": "",
      "configureFlags": "",
      "depsBuildBuild": "",
      "depsBuildBuildPropagated": "",
      "depsBuildTarget": "",
      "depsBuildTargetPropagated": "",
      "depsHostHost": "",
      "depsHostHostPropagated": "",
      "depsTargetTarget": "",
      "depsTargetTargetPropagated": "",
      "doCheck": "1",
      "doInstallCheck": "1",
      "mesonFlags": "",
      "name": "hello-2.12.1",
      "nativeBuildInputs": "/nix/store/wbjz30pdqxhg4hlw871l4p4y8n57w6ab-version-check-hook",
      "out": "/1rz4g4znpzjwh1xymhjpm42vipw92pr73vdgl6xs1hycac8kf2n9",
      "outputHashAlgo": "sha256",
      "outputHashMode": "recursive",
      "outputs": "out",
      "patches": "",
      "pname": "hello",
      "postInstallCheck": "stat \"${!outputBin}/bin/hello\"\n",
      "propagatedBuildInputs": "",
      "propagatedNativeBuildInputs": "",
      "src": "/nix/store/pa10z4ngm0g83kx9mssrqzz30s84vq7k-hello-2.12.1.tar.gz",
      "stdenv": "/nix/store/rkgsrccc7wnh3k5ila94lkvh0fvq89vz-stdenv-linux",
      "strictDeps": "",
      "system": "x86_64-linux",
      "version": "2.12.1"
    },
    "inputDrvs": {},
    "inputSrcs": [
      "/nix/store/an6si0s9azgz2wavyrvvlx8g76k4zifv-bash-5.2p37",
      "/nix/store/pa10z4ngm0g83kx9mssrqzz30s84vq7k-hello-2.12.1.tar.gz",
      "/nix/store/rkgsrccc7wnh3k5ila94lkvh0fvq89vz-stdenv-linux",
      "/nix/store/shkw4qm9qcw5sc5n1k5jznc83ny02r39-default-builder.sh",
      "/nix/store/vj1c3wf9c11a0qs6p3ymfvrnsdgsdcbq-source-stdenv.sh",
      "/nix/store/wbjz30pdqxhg4hlw871l4p4y8n57w6ab-version-check-hook"
    ],
    "name": "hello-2.12.1",
    "outputs": {
      "out": {
        "hashAlgo": "r:sha256"
      }
    },
    "system": "x86_64-linux"
  },
```

There are still some issues left though.

### The trouble with CA derivations as implemented in Nix

* The interop with IA derivations and the mixed store means there's still things that factor into the build, which we don't have a precise identity for. This it true for both inputs and outputs
* They have a differrent signature format at the `realizations` endpoint, but it's a bit of a mess.
* Realizations are not more trusted more than legacy signature format.
  - we would have to walk through the dependency tree starting at the leaves, verifying every step, instead
* They need rewriting, at least of the output path, and rewriting breaks stuff.
* IMO resolved derivations and dependency resolution should be user facing to make them understandable.

### let's get one of those signatures laut creates

We first build and run the signing part of the large VM test (this takes hours):
```
nix run github:mschwaig/laut/4f9b01b61e8f5a963831bc1160323bc86e0076d2#checks.x86_64-linux.large-sign.driver
./result-/bin/nixos-test-driver
```

Then we build and run the verification half:
```
nix run github:mschwaig/laut/4f9b01b61e8f5a963831bc1160323bc86e0076d2#checks.x86_64-linux.large-verify.driver
./result-/bin/nixos-test-driver
```

Now with this running, we can log into the WebUI at http://localhost:9001/, and go to the `traces` folder to find the signatures for `7gsw68f2iawn9q8vv04zh9xql14268pw`, and download them.

As a shortcut you can also play with the smaller tests, or get pretty much the resulting signature file from `tests/data/traces/signatures`.

I'm a bit annoyed myself by choosing S3 as the basis for the cache to demo this, because it would be much nicer to just `curl` a URL.

### and look at it

We're going to look at this using `https://gchq.github.io/CyberChef/`.

Basically there's two signatures in each file, since they are JWS they consist of 3 parts of BASE64 [].[].[], the 3rd of which is the actual signature.

If we past the first or second component of one of them into the input section cyberchef with this recipe https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)JSON_Beautify('%20%20%20%20',false,true), we get the actual contents:

First the header bits:
```

```

Then the payload:

```

```

We can also [diff the same signatures which are created by lix and Nix](ihttps://gchq.github.io/CyberChef/#recipe=Diff('%5C%5Cn%5C%5Cn%5C%5Cn','Character',true,true,false,false)&input=ewogICAgImluIjogewogICAgICAgICJyZHJ2X2pzb24iOiAiRXdVaVlpckVCcklsRGx4M3d4ci03VlZVa2FmUno2bGtnWVJiZkg2ZVJlQSIsCiAgICAgICAgInJkcnZfYXRlcm1fY2EiOiAia2NkZm1kbXc4bmFqOGZrYXZkaWQ4ZnhkYmptcWF3MjciLAogICAgICAgICJkZWJ1ZyI6IHsKICAgICAgICAgICAgImRydl9uYW1lIjogImJvb3RzdHJhcC1zdGFnZTAtZ2xpYmMtYm9vdHN0cmFwRmlsZXMiLAogICAgICAgICAgICAicmRydl9wYXRoIjogIi9uaXgvc3RvcmUva2NkZm1kbXc4bmFqOGZrYXZkaWQ4ZnhkYmptcWF3MjctYm9vdHN0cmFwLXN0YWdlMC1nbGliYy1ib290c3RyYXBGaWxlcy5kcnYiLAogICAgICAgICAgICAicmRydl9qc29uX3ByZWltYWdlIjogInsgLi4uIHNhbWUgZXhjZXB0IC4uLiBcIm91dHB1dHNcIjp7XCJvdXRcIjp7XCJoYXNoQWxnb1wiOlwicjpzaGEyNTZcIn19LFwic3lzdGVtXCI6XCJ4ODZfNjQtbGludXhcIn0iLAogICAgICAgICAgICAicmRydl9jb21wdXRlZF9wYXRoIjogIi9uaXgvc3RvcmUva2NkZm1kbXc4bmFqOGZrYXZkaWQ4ZnhkYmptcWF3MjctYm9vdHN0cmFwLXN0YWdlMC1nbGliYy1ib290c3RyYXBGaWxlcy5kcnYiLAogICAgICAgICAgICAicmRydl9hdGVybV9jYV9wcmVpbWFnZSI6IC4uLiBzYW1lIC4uLgogICAgICAgIH0KICAgIH0sCiAgICAib3V0IjogewogICAgICAgICJjYXN0b3JlLWVudHJ5IjogewogICAgICAgICAgICAib3V0IjogIkNpUVNJRXFOenJBTnRWWFRSVkkwWFZlXzZrWmlkTGNzRlJ3WXAwVEFTSUZQTzBTOEdBUSIKICAgICAgICB9LAogICAgICAgICJuaXgiOiB7CiAgICAgICAgICAgICJvdXQiOiB7CiAgICAgICAgICAgICAgICAiaGFzaEFsZ28iOiAicjpzaGEyNTYiLAogICAgICAgICAgICAgICAgInBhdGgiOiAiL25peC9zdG9yZS80eWpjcXZneHc4ZmN5MWg5ejV4bjJpbHByazJscW0xNy1ib290c3RyYXAtc3RhZ2UwLWdsaWJjLWJvb3RzdHJhcEZpbGVzIiwKICAgICAgICAgICAgICAgICJoYXNoIjogInNoYTI1NjoxOGJkaGxzaXFtczUyeW5hYWIxeTZrNDVqenpobDZ6MnAwcDBrYmEycGZiN2QwbTEzaXZuIgogICAgICAgICAgICB9CiAgICAgICAgfQogICAgfSwKICAgICJidWlsZGVyIjogewogICAgICAgICJyZWJ1aWxkX2lkIjogMzA3NDk5ODUzLAogICAgICAgICJzdG9yZV9yb290IjogIi9uaXgvc3RvcmUiLAogICAgICAgICJuaXhfZmxhdm9yIjogImxpeCIsCiAgICAgICAgIm5peF92ZXJzaW9uIjogIjIuOTEuMSIKICAgIH0KfQoKCnsKICAgICJpbiI6IHsKICAgICAgICAicmRydl9qc29uIjogIjgzX2RqUDYtUzFUbmNQS3NlcXdTQ0JyZ080MWNQNUJrYzVxck5vU0gzQWsiLAogICAgICAgICJyZHJ2X2F0ZXJtX2NhIjogImtjZGZtZG13OG5hajhma2F2ZGlkOGZ4ZGJqbXFhdzI3IiwKICAgICAgICAiZGVidWciOiB7CiAgICAgICAgICAgICJkcnZfbmFtZSI6ICJib290c3RyYXAtc3RhZ2UwLWdsaWJjLWJvb3RzdHJhcEZpbGVzIiwKICAgICAgICAgICAgInJkcnZfcGF0aCI6ICIvbml4L3N0b3JlL2tjZGZtZG13OG5hajhma2F2ZGlkOGZ4ZGJqbXFhdzI3LWJvb3RzdHJhcC1zdGFnZTAtZ2xpYmMtYm9vdHN0cmFwRmlsZXMuZHJ2IiwKICAgICAgICAgICAgInJkcnZfanNvbl9wcmVpbWFnZSI6ICJ7IC4uLiBzYW1lIGV4Y2VwdCAuLi4gXCJvdXRwdXRzXCI6e1wib3V0XCI6e1wiaGFzaEFsZ29cIjpcInNoYTI1NlwiLFwibWV0aG9kXCI6XCJuYXJcIn19LFwic3lzdGVtXCI6XCJ4ODZfNjQtbGludXhcIn0iLAogICAgICAgICAgICAicmRydl9jb21wdXRlZF9wYXRoIjogIi9uaXgvc3RvcmUva2NkZm1kbXc4bmFqOGZrYXZkaWQ4ZnhkYmptcWF3MjctYm9vdHN0cmFwLXN0YWdlMC1nbGliYy1ib290c3RyYXBGaWxlcy5kcnYiLAogICAgICAgICAgICAicmRydl9hdGVybV9jYV9wcmVpbWFnZSI6IC4uLiBzYW1lIC4uLgogICAgICAgIH0KICAgIH0sCiAgICAib3V0IjogewogICAgICAgICJjYXN0b3JlLWVudHJ5IjogewogICAgICAgICAgICAib3V0IjogIkNpUVNJRXFOenJBTnRWWFRSVkkwWFZlXzZrWmlkTGNzRlJ3WXAwVEFTSUZQTzBTOEdBUSIKICAgICAgICB9LAogICAgICAgICJuaXgiOiB7CiAgICAgICAgICAgICJvdXQiOiB7CiAgICAgICAgICAgICAgICAiaGFzaEFsZ28iOiAic2hhMjU2IiwKICAgICAgICAgICAgICAgICJtZXRob2QiOiAibmFyIiwKICAgICAgICAgICAgICAgICJwYXRoIjogIi9uaXgvc3RvcmUvNHlqY3F2Z3h3OGZjeTFoOXo1eG4yaWxwcmsybHFtMTctYm9vdHN0cmFwLXN0YWdlMC1nbGliYy1ib290c3RyYXBGaWxlcyIsCiAgICAgICAgICAgICAgICAiaGFzaCI6ICJzaGEyNTY6MThiZGhsc2lxbXM1MnluYWFiMXk2azQ1anp6aGw2ejJwMHAwa2JhMnBmYjdkMG0xM2l2biIKICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0sCiAgICAiYnVpbGRlciI6IHsKICAgICAgICAicmVidWlsZF9pZCI6IDE2OTAwMDQyMjEsCiAgICAgICAgInN0b3JlX3Jvb3QiOiAiL25peC9zdG9yZSIsCiAgICAgICAgIm5peF9mbGF2b3IiOiAibml4IiwKICAgICAgICAibml4X3ZlcnNpb24iOiAiMi4yOC4zIgogICAgfQp9).

This leads us into discussing some aspects of laut:
* the quorum stuff
* looking at verification
* talking about support for IA sigantures
* talking link to builder software state and remote attestation

---

What do people think about vibenix?

My panel at NixCon:
https://discourse.nixos.org/t/input-for-supply-chain-security-panel-at-nixcon/68172
Please ask questions, and if you know somebody who should be involved recommend them to me.

