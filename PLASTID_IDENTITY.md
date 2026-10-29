# Plastid naming and migration policy

The product, app and repository identity is **Plastid**. Earlier project/app labels are retired and may appear only in a historical reference, saved data migration, or a temporary firmware compatibility parser.

Current Pi package: `Plastid_App_v03`, `plastid_lab.html`, `run_plastid_lab.py`, `pi_bridge_server.py`. Browser app data is stored under `plastid-lab`, automatically copying legacy data only when no Plastid key exists; legacy storage is not deleted. Exports use Plastid filenames.

**Physical firmware caveat:** ESP32-S3 v0.1.0 has been uploaded and still announces its old project identity. The Pi bridge temporarily accepts it. Do not erase or overwrite the board to force an immediate rename. The next deliberate firmware release should use `\"project\":\"Plastid\"` with a versioned handshake.

The setup branch currently contains old-name staging paths. Preserve their history and migrate the source into `plastid/` deliberately, rather than silently mutating a live app. HappyJarz remains a separate project and is not renamed.
