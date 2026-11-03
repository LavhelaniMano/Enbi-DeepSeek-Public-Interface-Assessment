# One-minute project introduction video

## Script

Hi, I’m **[your name]**. My project examines how AI assistants respond to banking, fraud and privacy questions.

I observed Enbi, Nedbank’s public chatbot, with a structured set of prompts. I added DeepSeek because it is a general-purpose model, to explore how a broader assistant handles banking-related safety, privacy and factual claims.

I recorded 29 benign and eight adversarial Enbi runs, plus 37 manually submitted DeepSeek prompts. Enbi gave stable guidance to repeated balance questions, and no account-specific data appeared in the adversarial responses. DeepSeek often set boundaries, but some financial and contact claims went unverified. In one response, it misidentified its creator.

This small exploratory study is not a full security audit or model ranking. My takeaway: preserve evidence, verify confident claims and be clear about what the results can show. Thank you.

## Simple recording plan

Aim for **about 60 seconds**. The script is about 130 words; read at a measured pace and pause briefly between paragraphs. If you run over a minute, trim a sentence rather than rushing.

| Time | What to show |
| --- | --- |
| 0–8 sec | Show your face and introduce yourself. |
| 8–22 sec | Show the project title or report cover while explaining the question and why you added DeepSeek. |
| 22–36 sec | Show the results summary. |
| 36–48 sec | Show one Enbi screenshot, then the DeepSeek response excerpts. |
| 48–57 sec | Return to your face or the report’s limitations and takeaway. |
| 57–60 sec | Thank the viewer and end the recording. |

## How to make and submit it

1. Replace **[your name]** and practice once with a timer. The script is about 130 words; if you run over a minute, trim a sentence rather than rushing.
2. Record horizontally in a quiet, well-lit place. Put the camera at eye level, keep your face in frame, and speak clearly. A phone or computer camera is enough.
3. If you share your screen, open the report or screenshots in advance and enlarge them so the text is readable. Keep private information, account details and unrelated tabs out of view.
4. Record one or two takes, then watch the video once to check that the sound is clear and no private information is visible. Trim the beginning or end if needed.
5. Save an MP4 with a clear name such as `Project_Introduction_[YourName].mp4`.
6. Upload it to your chosen file-sharing service, set access so the intended reviewers can view it, and test the link in a private/incognito window or while signed out. Avoid making it publicly searchable if a restricted share link will work.
7. Paste the working share link into the **One-minute introduction video** field in `docs/PR_Project_Response.tex`, replacing the placeholder. Then rebuild the PDF from the same folder (`pdflatex PR_Project_Response.tex`) so `docs/PR_Project_Response.pdf` shows the link. Keep the local video file as your backup.

## Before recording

- Say “exploratory comparison,” not “security proof” or “model ranking.”
- The DeepSeek prompts were manually submitted; the project did not train or build DeepSeek.
- Do not show login sessions, personal information, private messages or credentials.
